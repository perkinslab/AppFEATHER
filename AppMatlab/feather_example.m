function []=feather_example()
    %{
    example which uses FEATHER.

    Path must be set properly 
    %}
    feather_assertions();
    pwd_res = pwd;
    base_feather_dir = feather_path(pwd_res);
    % read the input file
    input_csv = [base_feather_dir filesep 'Data' filesep  ...
                 '3D300_3800_Image0909DeflConcat.csv'];
    base_path = [base_feather_dir filesep 'AppPython' filesep];
    [trigger_time,dwell_time,spring_constant] = ...
        feather_meta_header(input_csv);
    skip_rows=2;
    skip_cols=0;
    data = csvread(input_csv,skip_rows,skip_cols);
    % get the individual columns, for plotting purposes
    time = data(:,1);
    separation = data(:,2);
    force = data(:,3);
    % get the force extension curve object to use
    obj = fec(time,separation,force,trigger_time,dwell_time,...
              spring_constant);
    % get the feather-specific options to use
    threshold = 1e-3;
    tau = 2e-2;
    python_binary = feather_binary();
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
