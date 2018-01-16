// Use modern global access method, strict compilation
#pragma rtGlobals=3	

#include "::Feather"
#include ":::UtilIgorPro:Util:PlotUtil"
#include ":::UtilIgorPro:Util:IoUtil"

#pragma ModuleName = ModMainFeather


Static StrConstant DEF_PATH_NAME = "Example"
Static StrConstant DEF_INPUT_REL_TO_BASE ="AppIgor:Example:feather_example.pxp"

Static Function Main_Windows()
	// Runs a simple IWT on patrick's windows setup
	ModMainFEATHER#Main()
End Function 

Static Function Main_Mac()
	// Runs a simple IWT on patrick's mac setup 
	ModMainFEATHER#Main()
End Function

Static Function Main([base,input_file])
	// // This function shows how to use the IWT code
	// Args:
	//		base: the folder where the Research Git repository lives 
	//		input_file: the pxp to load. If not present, defaults to 
	//		<base>DEF_INPUT_REL_TO_BASE
	String base,input_file
	if (ParamIsDefault(base))
		base = ModIoUtil#pwd_igor_path(DEF_PATH_NAME,n_up_relative=3)
	EndIf
	if (ParamIsDefault(input_file))
		input_file  = base +DEF_INPUT_REL_TO_BASE
	EndIf
	KillWaves /A/Z
	ModPlotUtil#KillAllGraphs()
	// IWT options
	Struct FeatherOptions opt
	opt.tau = 0
	opt.threshold = 1e-3
	opt.tau = 2e-2
	// Add the meta information
	opt.trigger_time = 0.382
	opt.dwell_time = 0.992
	opt.spring_constant = 6.67e-3
	// add the file information
	opt.meta.path_to_input_file = input_file
	opt.meta.path_to_research_directory = base
	// Make the output waves
	Struct FeatherOutput output
	Make /O/N=0, output.event_starts
	// Execte the command
	ModFeather#feather(opt,output)
	// Make a fun plot wooo
	LoadData /O/Q/R (ModOperatingSystemUtil#sanitize_path(input_file))
	Wave Y =  $("Image0994Force")
	Wave X =  $("Image0994Sep")
	Display Y vs X
	Variable n_events = DimSize(output.event_starts,0)
	Variable i
	for (i=0; i<n_events; i+=1)
		Variable event_idx = output.event_starts[i]
		ModPlotUtil#axvline(X[event_idx])
	endfor
	ModPlotUtil#xlabel("Extension (m)")
	ModPlotUtil#ylabel("Force (N)")
	Edit output.event_starts as "Predicted Event Indices in Wave"
End Function
