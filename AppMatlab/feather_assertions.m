function [] = feather_assertions()
    %{
    Returns: 
        python_binary: the location of the python binary. throws an error
            if it can't be found. 
    %}
    err_msg = ['FEATHER untested on MATLAB < 2017. Detected: ' version];
    assert(~verLessThan('matlab','2017'),err_msg);
end
