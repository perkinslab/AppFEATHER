function []=feather_example()
    %{
    example which uses FEATHER.

    Path must be set properly 
    %}
    delim = '/';
    pwd_res = pwd;
    dir_str = strsplit(pwd_res,{delim,'\'},'CollapseDelimiters',true);
    base = join(dir_str(1,1:end-1),delim);
	% base_path should be correct if base is 
    base_path = [base{1},'/AppPython/'];
    % read the input file
    input_csv = '../Data/example.csv';
    data = csvread(input_csv);
    % get the individual columns, for plotting purposes
    time = data(:,1);
    separation = data(:,2);
    force = data(:,3);
    % in this case, the instrument records  meta information we need 
    trigger_time = 0.382;
    dwell_time = 0.992;
    spring_constant = 6.67e-3;
    % get the force extension curve object to use
    obj = fec(time,separation,force,trigger_time,dwell_time,...
              spring_constant);
    % get the feather-specific options to use
    threshold = 1e-3;
    tau = 2e-2;
    if (ismac)
        python_binary = '//anaconda/bin/python2 ';
    else
        python_binary = 'C:/ProgramData/Anaconda2/python.exe ';        
    end
    opt = feather_options(threshold,tau,base_path,python_binary);
    % get the predicted event locations
    indices = feather(obj,opt); 
    disp('Events found at the following indices: ');
    disp(indices);
    clf;
    hold all;
    tmp_size = size(obj.force);
    n_rounded = round(tmp_size(1)/10);
    obj.force = obj.force - median(obj.force(1:n_rounded));
    conv = -1e12;
    plot(obj.time,obj.force*conv)
    for i=1:length(indices)
        plot(obj.time(indices(i)),obj.force(indices(i))*conv,'ro')
    end
    xlabel('Time (s)');
    ylabel('Force (pN)');
end
