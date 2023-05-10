# BeamAlignment
Code for aligning a laser with a nanotip ion source.

This project comprises part of my senior honors thesis in physics at Brown University. I work in a group working towards sequencing proteins from single molecules, and one of the techincal challenges of that workflow is aligning a laser beam with a nanotip ion source – a drawn glass capillary nanometers wide at the very tip.

The workflow involves rasterscanning the laser over the nanotip while recording the power that is transmitted to a power sensor. This is accomplished by the LabView project Alignment_Controls.lvproj and the C# script MirrorProtocol.sln. Data of the voltages appplied to a steering mirror, as well as beam position and power measurements from a sensor, are analyzed the files main.py, scan_analysis.py, and visualizers.py. The get_voltage_arrat.py file contains a function that provides an array of distinct voltages to apply to the steering mirror when interfaced with the LabView VI.

The final part of the project that has yet to be completed involves interfacing the scan analysis python methods in LabView to make the alignment procedure fully automated.
