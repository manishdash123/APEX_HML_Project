/******************************************************************************
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
*******************************************************************************/

#include "TacosGreedy.h"
#include <cassert>
#include <iostream>
#include <limits>
#include <fstream>

using namespace Tacos;

TacosGreedy::TacosGreedy(const std::shared_ptr<Topology> topology, const std::shared_ptr<Collective> collective) noexcept
    : topology(topology), collective(collective) {
    // set values
    npusCount = topology->getNpusCount();
    chunksCount = collective->getChunksCount();
    chunkSize = collective->getChunkSize();

    // create TACOS network representation
    network = std::make_unique<TacosNetwork>(topology, chunkSize);
}

Time TacosGreedy::solve() noexcept {
    // allocate memory for contains
    auto contains = std::make_shared<Contains>(chunksCount, std::vector<bool>(npusCount, false));

    // mark preconditions as true
    for (auto [chunk, npu] : collective->getPrecondition()) {
        (*contains)[chunk][npu] = true;
    }

    // mark current time
    Time currentTime = 0;
    Time collectiveTime = 0;

    // initialize event queue
    eventQueue.schedule(0);

    std::cout<<"TACOS SOLVE"<<std::endl;
    std::ofstream file("output.csv", std::ofstream::out | std::ofstream::app); // Open in append mode

    while (!eventQueue.empty()) {
        // get current time
        currentTime = eventQueue.pop();

        // initialize (randomized) requests
        auto requests = initializeRequests(contains);

        // if this is true, something happened during prepareBacktracking process
        // so should update resulting collective time.
        const auto shouldUpdateCollTime = prepareBacktracking(file, requests, currentTime, contains);
        if (shouldUpdateCollTime) {
            // update collective time to current time
            collectiveTime = currentTime;
        }

        if (requests->empty()) {
            // nothing is in the request pool
            // do nothing and wait until everything arrives dest
            network->reset();
            continue;
        }

        // counters for this timestep
        int totalChunksCount = requests->size();
        auto successfulMatchingCount = 0;

        for (auto [chunk, dest] : *requests) {
            const auto incomingNpus = network->incomingNpus(dest);
            auto candidateLinks = std::set<std::pair<LinkId, Time>>();

            // choose candidate links by iterating over incoming NPUs
            for (auto src : incomingNpus) {
                if ((*contains)[chunk][src]) {
                    const auto selectedLink = std::make_pair(src, dest);
                    const auto linkWeight = topology->linkTime(selectedLink, chunkSize);
                    const auto linkTime = currentTime + linkWeight;
                    candidateLinks.emplace(selectedLink, linkTime);
                }
            }

            if (candidateLinks.empty()) {
                // no match can be made
                continue;
            }

            // select shortest link -- matching made
            const auto [selectedLink, linkTime] = selectBestLink(candidateLinks);

            // update chunk and link time
            successfulMatchingCount++;
            network->setProcessingChunk(selectedLink, chunk);
            network->setLinkTime(selectedLink, linkTime);
            network->setLinkStartTime(selectedLink, currentTime);
            eventQueue.schedule(linkTime);

            // remove this link from matching -- prevent congestion
            network->removeLink(selectedLink);
        }

        // reset topology and continue
        network->reset();
    }

    file.close();

    // all matching has been finished
    // return measured collective time
    return collectiveTime;
}

std::shared_ptr<TacosGreedy::RequestSet>
TacosGreedy::initializeRequests(const std::shared_ptr<Contains> contains) noexcept {
    auto requests = std::make_shared<RequestSet>();

    for (const auto [chunk, dest] : collective->getPostcondition()) {
        assert(chunk >= 0);
        assert(0 <= dest && dest < npusCount);

        if (!(*contains)[chunk][dest]) {
            // mark chunks that hasn't arrived dest yet
            requests->emplace_back(chunk, dest);
        }
    }

    // shuffle queue
    std::shuffle(requests->begin(), requests->end(), randomEngine);
    return requests;
}

bool TacosGreedy::prepareBacktracking(std::ofstream& file, std::shared_ptr<RequestSet> requests, const Time currentTime,
                                      std::shared_ptr<Contains> contains) noexcept {
    auto totalArrival = 0;
    auto arrivalsCount = 0;
    auto discardedCount = 0;
    auto replacedCount = 0;

    std::cout<<"Prepare Backtracking"<<std::endl;

    for (auto src = 0; src < npusCount; src++) {
        for (auto dest = 0; dest < npusCount; dest++) {
            // iterate over all existing links
            if (!topology->connected(src, dest)) {
                continue;
            }

            // check link time
            const auto link = std::make_pair(src, dest);
            const auto linkTime = network->linkTime(link);
            const auto linkStartTime = network->linkStartTime(link);

            if (linkTime <= 0) {
                // nothing is happening on this link: just skip
                continue;
            }

            if (currentTime < linkTime) {
                // transfer in progress: cannot use this link at this point
                network->removeLink(link);
                continue;
            }

            // one transmission has finished
            totalArrival++;

            // check this chunk should be replaced
            auto chunk = network->processingChunk(link);

            if ((*contains)[chunk][dest]) {
                // already contains this chunk
                // so this chunk should be either replaced or discarded

                // check if any replacement candidate exists
                auto replaceCandidate = std::vector<ChunkId>();

                // iterate over all requests to find a chunk rc
                // where request[rc][dest] = true, contains[rc][src] = true, contains[rc][dest] = false
                for (const auto [rc, rd] : *requests) {
                    if (rd == dest && (*contains)[rc][src] && !(*contains)[rc][dest]) {
                        // rc has arrived at src but not at dest
                        // so rc can be a replacement candidate
                        replaceCandidate.push_back(rc);
                    }
                }

                if (replaceCandidate.empty()) {
                    // this src -> dest has already been finished
                    // nothing to send
                    discardedCount++;
                    network->removeLink(link);  // disable this link (for optimization)
                    continue;
                }

                // random choice one candidate
                auto distribution = std::uniform_int_distribution<>(0,
                                                                    replaceCandidate.size() - 1);  // define the range
                const auto index = distribution(randomEngine);
                chunk = replaceCandidate[index];
                replacedCount++;
            }

            // a chunk has arrived at dest
            arrivalsCount++;
            (*contains)[chunk][dest] = true;  // chunk arrived at dest

            // FIXME: (src -> dest) of (chunk) is happening at time linkStartTime ==========================
            std::cout << "[At time " << linkStartTime << "] Send Chunk " << chunk << " from " << src << " -> " << dest << std::endl;
            file << linkStartTime << "," << chunk << "," << src << "," << dest << std::endl;
            // FIXME: ====================================================================================

            // reset chunk and link time
            network->setProcessingChunk(link, -1);
            network->setLinkTime(link, -1);
            network->setLinkStartTime(link, -1);

            // remove this (chunk, dest) from the request pool
            auto idx = std::find(requests->begin(), requests->end(), std::make_pair(chunk, dest));
            requests->erase(idx);
        }
    }
    // return true if any arrival or replacement happens
    return (arrivalsCount > 0) || (replacedCount > 0);  // true if any arrival or replacement happens
}

std::pair<LinkId, Time> TacosGreedy::selectBestLink(const CandidateLinkSet& candidateLinks) noexcept {
    auto minLinkTime = std::numeric_limits<double>::max();
    LinkId selectedLink;

    // select link that has minimum link time
    // candidateLInks is already shuffled, so no need for additional shuffling
    // if multiple links are colliding.
    for (auto [link, linkTime] : candidateLinks) {
        if (linkTime < minLinkTime) {
            minLinkTime = linkTime;
            selectedLink = link;
        }
    }

    return {selectedLink, minLinkTime};
}
