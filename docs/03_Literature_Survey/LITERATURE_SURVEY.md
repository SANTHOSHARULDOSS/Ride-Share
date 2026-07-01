# Literature Survey

A review of existing research, literature, and platforms in the domain of smart urban transportation, carpooling heuristics, and route-matching optimizations.

---

## 1. Research Paper Reviews

### Paper 1: "Dynamic Ride-Sharing Systems: A Survey of Route Optimization and Matching Algorithms"
* **Key Findings:** Radial search methods (radius-based matches) introduce detour inefficiencies. The paper suggests segment-based route partitioning where a driver's line is treated as a series of sequential coordinate pairs rather than a single starting/ending vector.
* **Relevance to MVP:** Guided the development of our sequential index matching logic ($i < j$), ensuring that travel direction constraints are checked before assessing detour thresholds.

### Paper 2: "Heuristics for Dynamic Multi-Hop Ride-Sharing Problems"
* **Key Findings:** Explains the mathematical application of the Haversine formula to compute great-circle distance on the earth's surface. High-performance matching queries can run in $O(N)$ if sequential waypoint limits are capped.
* **Relevance to MVP:** Formed the core of our `haversine_distance` formula inside the matching logic.

---

## 2. Competitive Analysis

| System Features | Commercial Taxi Apps (Uber/Lyft) | Traditional Carpooling | AI-Based Ride-Sharing MVP |
| :--- | :--- | :--- | :--- |
| **Routing Focus** | Point-to-point on-demand | Static route (pre-negotiated) | **Dynamic Waypoints matching** |
| **API Costs** | High (Google Maps SDK billing) | None (Manual communication) | **Free OpenStreetMap/Leaflet integration** |
| **Offline Resilience** | Poor (Crashes on network drop) | None | **Service Worker Offline Demo fallbacks** |
| **Detour Overhead** | Not optimized for path sharing | Manual negotiation | **Algorithmic walk detour scoring** |
