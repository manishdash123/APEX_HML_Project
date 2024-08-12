/******************************************************************************
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
*******************************************************************************/

#pragma once

#include "common/Type.hh"
#include "congestion_aware/BasicTopology.hh"

using namespace NetworkAnalytical;

namespace NetworkAnalyticalCongestionAware {

class Mesh2D final : public BasicTopology {
 public:
  /**
   * Constructor.
   *
   * @param npus_count number of npus in a ring
   * @param bandwidth bandwidth of link
   * @param latency latency of link
   * @param bidirectional true if ring is bidirectional, false otherwise
   */
  Mesh2D(int npus_count, Bandwidth bandwidth, Latency latency) noexcept;

  /**
   * Implementation of route function in Topology.
   */
  [[nodiscard]] Route route(DeviceId src, DeviceId dest)
      const noexcept override;

 private:
  /// true if the ring is bidirectional, false otherwise
  bool bidirectional;
  int width;
  int height;
};

} // namespace NetworkAnalyticalCongestionAware
