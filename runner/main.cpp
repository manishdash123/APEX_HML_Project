/******************************************************************************
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
*******************************************************************************/

#include "AllGather.h"
#include "Mesh2D.h"
#include "Torus2D.h"
#include "Hypercube3D.h"
#include "Torus3D.h"
#include "TacosGreedy.h"
#include "Timer.h"
#include <iostream>

using namespace Tacos;

int main(int argc, char *argv[]) {
    // FIXME: Experimental Configuration =========================================================
    int _width = atoi(argv[1]);  // 2D Mesh width
    //int height = width;  // 2D Mesh height
    int _linkLatency = atoi(argv[2]);  // ns
    int _linkBandwidth = atoi(argv[3]);  // GB/s
    int _allGatherSize = atoi(argv[4]);  // MB
    int _chunksCountPerAllGather = atoi(argv[5]);  // how many chunks per each All-Reduce collective

    //std::cout<<"Enter <_width> <_linkLatency> <_linkBandwidth> <_allGatherSize> <_chunksCountPerAllGather> :";

    //std::cin>>_width>>_linkLatency>>_linkBandwidth>>_allGatherSize>>_chunksCountPerAllGather;
    // FIXME: ====================================================================================

    const auto width = _width;  // 2D Mesh width
    const auto height = _width;  // 2D Mesh height
    const auto linkLatency = _linkLatency;  // ns
    const auto linkBandwidth = _linkBandwidth;  // GB/s
    const auto allGatherSize = _allGatherSize;  // MB
    const auto chunksCountPerAllGather = _chunksCountPerAllGather;  // how many chunks per each All-Reduce

    // set print precision
    fixed(std::cout);
    std::cout.precision(2);

    // calculate link alpha-beta
    const auto link_alpha_us = linkLatency / 1000.0;
    const auto link_beta_us_per_MB = 1'000'000.0 / (linkBandwidth * 1'024.0);  // us/MB
    const auto linkAlphaBeta = std::make_pair(link_alpha_us, link_beta_us_per_MB);

    // construct topology
    const auto topology = std::make_shared<Mesh2D>(width, height, linkAlphaBeta);
    const auto npusCount = topology->getNpusCount();

    // calculate chunk size
    const auto collSizePerNpu = static_cast<double>(allGatherSize) / npusCount;
    const auto chunkSize = collSizePerNpu / chunksCountPerAllGather;

    // create collective
    const auto collective = std::make_shared<AllGather>(npusCount, chunkSize, chunksCountPerAllGather);
    const auto chunksCount = collective->getChunksCount();

    // print metadata
    std::cout << "[2D Mesh Information]" << std::endl;
    std::cout << "\t" << "#NPUs: " << npusCount << std::endl;
    std::cout << "\t" << "LinkLatency: " << linkLatency << " ns (" << link_alpha_us << " us)" << std::endl;
    std::cout << "\t" << "LinkBandwidth: " << linkBandwidth << " GB/s (" << link_beta_us_per_MB << " us/MB)" << std::endl;
    std::cout << std::endl;

    std::cout << "[All-Reduce Information]" << std::endl;
    std::cout << "\t" << "#Chunks/NPU: " << chunksCountPerAllGather << std::endl;
    std::cout << "\t" << "Chunk Size: " << chunkSize << " MB" << std::endl;
    std::cout << "\t" << "All-Reduce Size: " << allGatherSize << " MB" << std::endl;
    std::cout << std::endl;

    // create timer
    auto solverTimer = Timer("PathSolver");

    // create solver and solve
    std::cout << "[Synthesizing Collective Algorithm]" << std::endl;

    solverTimer.start();
    auto solver = TacosGreedy(topology, collective);
    const auto collectiveTime = solver.solve();
    solverTimer.stop();
    const auto synthesisTime = solverTimer.getTime("ms");

    std::cout << "[Synthesis Finished]" << std::endl;
    std::cout << std::endl;

    // print synthesis result

    std::cout << "[Synthesis Result]" << std::endl;
    std::cout << "\tAll-Gather Time: " << collectiveTime << " us" << std::endl;
    std::cout << "\tAll-Reduce Time: " << collectiveTime * 2 << " us" << std::endl;
    std::cout << "\tSynthesis Time: " << synthesisTime << " ms" << std::endl;

    // terminate
    return 0;
}
