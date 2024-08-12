/******************************************************************************
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
*******************************************************************************/

#include "congestion_aware/Mesh2D.hh"
#include <cassert>
#include <cmath>

using namespace NetworkAnalyticalCongestionAware;

Mesh2D::Mesh2D(
    const int npus_count,
    const Bandwidth bandwidth,
    const Latency latency) noexcept
    : BasicTopology(npus_count, npus_count, bandwidth, latency) {
  assert(npus_count > 0);
  assert(bandwidth > 0);
  assert(latency >= 0);

  // get width and height
  width = static_cast<int>(std::sqrt(npus_count));
  height = width;

  // currently, only square mesh is supported
  assert(width * height == npus_count);

  // connect width-wise
  for (auto h = 0; h < height; h++) {
    for (auto w = 0; w < width - 1; w++) {
      const auto dest_w = w + 1;
      const auto src = (h * width) + w;
      const auto dest = (h * width) + dest_w;

      connect(src, dest, bandwidth, latency, true);
    }
  }

  // connect height-wise
  for (auto w = 0; w < width; w++) {
    for (auto h = 0; h < height - 1; h++) {
      const auto dest_h = h + 1;
      const auto src = (h * width) + w;
      const auto dest = (dest_h * width) + w;

      connect(src, dest, bandwidth, latency, true);
    }
  }
}

Route Mesh2D::route(DeviceId src, DeviceId dest) const noexcept {
  // assert npus are in valid range
  assert(0 <= src && src < npus_count);
  assert(0 <= dest && dest < npus_count);
  assert(src != dest);

  // construct empty route
  auto route = Route();

  // get (h, w) format of the src and dest
  const auto src_h = src / width;
  const auto src_w = src % width;
  const auto dest_h = dest / width;
  const auto dest_w = dest % width;

  // run width-wise routing
  const auto dir_w = (dest_w > src_w) ? 1 : -1;
  const auto dir_h = (dest_h > src_h) ? 1 : -1;

  auto current_w = src_w;
  auto current_h = src_h;

  // first run width-wise routing
  while (current_w != dest_w) {
    // append current position
    const auto current = (current_h * width) + current_w;
    route.push_back(devices[current]);

    // move width-wise
    current_w += dir_w;
  }

  // then, run height-wise
  while (current_h != dest_h) {
    // append current position
    const auto current = (current_h * width) + current_w;
    route.push_back(devices[current]);

    // move height-wise
    current_h += dir_h;
  }

  // finally, add dest to the path
  route.push_back(devices[dest]);

  // return the constructed route
  return route;
}
