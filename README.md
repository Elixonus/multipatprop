# multipatprop
Multipath propagation simulation using ray-casting method and finite element analysis.

## Algorithm
Transmitter sends signals in every direction with a limited number of starting paths.
Receiver collects all the propagated paths (paths that made it to the receiver) and records the data of these.
Propagated path is determined by whether the signal reaches within a certain distance of the receiver.
The signals may bounce off of reflective interferers and will still count as propagated.
However, every collision the signal makes with an interferer, the energy of the signal decays exponentially.

The algorithm described above allows us to make a visualization of all the paths that reach the target.

To make the time energy graph, which describes the rate of energy (non-cumulative) received by the receiver from all direction at any time,
the time is separated into bars and for every path propagated, the bar with the corresponding travel time is selected to be added by the final energy of it.
