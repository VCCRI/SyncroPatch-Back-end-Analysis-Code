
def generate_warnings(A_fast,A_slow ,tau_fast,tau_slow,actual_sweep,summary_sweep,sweep_length,max_model,rsquare,rsq_thresh,amp_thresh, summary_sweep_voltage, sweep_voltage):
    warning = ''
    # Comprehensive Warning generation for the sweep of interest
    if actual_sweep == summary_sweep:
        # Ensure the tau values take on a logical range (positive)
        #if summary_sweep < 11:
        if summary_sweep_voltage > -80:
            if tau_fast > 0 and tau_slow > 0:
                if tau_fast * 1e-3 <= sweep_length:
                    if tau_slow * 1e-3 <= sweep_length:
                        if max_model >= amp_thresh:
                            if rsquare >= rsq_thresh:
                                if A_fast < 0:
                                    if A_slow < 0:
                                        warning = 'Both amplitudes are negative'
                                    else:
                                        warning = 'A_fast amplitude negative'
                                else:
                                    if A_slow < 0:
                                        warning = 'A_slow amplitude negative'
                                    else:
                                        if A_fast > 2000:
                                            if A_slow > 2000:
                                                warning = 'Both amplitudes too high'
                                            else:
                                                warning = 'A_fast amplitude too high'
                                        else:
                                            if A_slow > 2000:
                                                warning = 'A_slow amplitude too high'
                            else:
                                if A_fast < 0:
                                    if A_slow < 0:
                                        warning = 'Rsquare less than the supplied threshold and both amplitudes negative'
                                    else:
                                        warning = 'Rsquare less than the supplied threshold and A_fast amplitude negative'
                                else:
                                    if A_slow < 0:
                                        warning = 'Rsquare less than the supplied threshold and A_slow amplitude negative'
                                    else:
                                        if A_fast > 2000:
                                            if A_slow > 2000:
                                                warning = 'Rsquare less than the supplied threshold and both amplitudes too high'
                                            else:
                                                warning = 'Rsquare less than the supplied threshold and A_fast amplitude too high'
                                        else:
                                            if A_slow > 2000:
                                                warning = 'Rsquare less than the supplied threshold and A_slow amplitude too high'
                                            else:
                                                warning = 'Rsquare less than the supplied threshold'
                        else:
                            if A_fast < 0:
                                if A_slow < 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both amplitudes negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both amplitudes negative'
                                else:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and A_fast amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and A_fast amplitude negative'
                            else:
                                if A_slow < 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and A_slow amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and A_slow amplitude negative'
                                else:
                                    if A_fast > 2000:
                                        if A_slow > 2000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both amplitudes too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both amplitudes too high'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and A_fast amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and A_fast amplitude too high'
                                    else:
                                        if A_slow > 2000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and A_slow amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and A_slow amplitude too high'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor'
                    else:
                        if max_model >= amp_thresh:
                            if A_fast < 0:
                                if A_slow < 0:
                                    warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes neagtive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes neagtive'
                                else:
                                    warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'
                            else:
                                if A_slow < 0:
                                    warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'
                                else:
                                    if A_fast > 2000:
                                        if A_slow > 2000:
                                            warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes too high'
                                        else:
                                            warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude too high'
                                    else:
                                        if A_slow > 2000:
                                            warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'
                                        else:
                                            warning = 'The tau_slow parameter has taken on a value longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration'
                        else:
                            if A_fast < 0:
                                if A_slow < 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes are negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes are negative'
                                else:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'
                            else:
                                if A_slow < 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'
                                else:
                                    if A_fast > 2000:
                                        if A_slow > 2000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes too high'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude too high'
                                    else:
                                        if A_slow > 2000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration'
                else:
                    if tau_slow * 1e-3 > sweep_length:
                        if max_model >= amp_thresh:
                            if A_fast < 0:
                                if A_slow < 0:
                                    warning = 'Both tau parameters have taken on values longer than the sweep duration and both amplitudes negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes negative'

                                else:
                                    warning = 'Both tau parameters have taken on values longer than the sweep duration and A_fast amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude negative'

                            else:
                                if A_slow < 0:
                                    warning = 'Both tau parameters have taken on values longer than the sweep duration and A_slow amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude negative'
                                else:
                                    if A_fast > 2000:
                                        if A_slow > 2000:
                                            warning = 'Both tau parameters have taken on values longer than the sweep duration and both amplitudes too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes too high'

                                        else:
                                            warning = 'Both tau parameters have taken on values longer than the sweep duration and A_fast amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude too high'

                                    else:
                                        if A_slow > 2000:
                                            warning = 'Both tau parameters have taken on values longer than the sweep duration and A_slow amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude too high'
                                        else:
                                            warning = 'Both tau parameters have taken on values longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration'
                        else:
                            if A_fast < 0:
                                if A_slow < 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and both amplitudes negative'

                                else:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude negative'
                            else:
                                if A_slow < 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude negative'
                                else:
                                    if A_fast > 2000:
                                        if A_slow > 2000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and both amplitudes too hogh'

                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude to high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude too high'
                                    else:
                                        if A_slow > 2000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude too high'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration'
                    else:
                        if max_model >= amp_thresh:
                            if A_fast < 0:
                                if A_slow < 0:
                                    warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes negative'

                                else:
                                    warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'

                            else:
                                if A_slow < 0:
                                    warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'

                                else:
                                    if A_fast > 2000:
                                        if A_slow > 2000:
                                            warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes too high'
                                        else:
                                            warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude too high'
                                    else:
                                        if A_slow > 2000:
                                            warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'
                                        else:
                                            warning = 'The tau_fast parameter has taken on a value longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration'
                        else:
                            if A_fast < 0:
                                if A_slow < 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes negative'
                                else:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'
                            else:
                                if A_slow < 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'
                                else:
                                    if A_fast > 2000:
                                        if A_slow > 2000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes too high'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude too high'
                                    else:
                                        if A_slow > 2000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration'
            else:
                if tau_fast < 0:
                    if tau_slow > 0:
                        if A_fast < 0:
                            if A_slow < 0:
                                warning = 'tau_fast negative and both amplitudes negative'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold and both amplitudes negative'
                                    if max_model <= amp_thresh:
                                        warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes negative'

                            else:
                                warning = 'tau_fast negative and A_fast amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold and A_fast amplitude negative'
                                    if max_model <= amp_thresh:
                                        warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude negative'
                        else:
                            if A_slow < 0:
                                warning = 'tau_fast negative and A_slow amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold and A_slow amplitude negative'
                                    if max_model <= amp_thresh:
                                        warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude negative'
                            else:
                                if A_fast > 2000:
                                    if A_slow > 2000:
                                        warning = 'tau_fast negative and both amplitudes too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and both amplitudes too high'
                                            if max_model <= amp_thresh:
                                                warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes too high'

                                    else:
                                        warning = 'tau_fast negative and A_fast amplitude too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and A_fast amplitude too high'
                                            if max_model <= amp_thresh:
                                                warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude too high'
                                else:
                                    if A_slow > 2000:
                                        warning = 'tau_fast negative and A_slow amplitude too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and A_slow amplitude too high'
                                            if max_model <= amp_thresh:
                                                warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude too high'
                                    else:
                                        warning = 'tau_fast negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold'
                                            if max_model <= amp_thresh:
                                                warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low'
                    else:
                        if A_fast < 0:
                            if A_slow < 0:
                                warning = 'tau values are both negative and both amplitudes are negative'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and both amplitudes are negative'
                                    if max_model < amp_thresh:
                                        warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes are negative'

                            else:
                                warning = 'tau values are both negative and A_fast amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and A_fast amplitude negative'
                                    if max_model < amp_thresh:
                                        warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude negative'

                        else:
                            if A_slow < 0:
                                warning = 'tau values are both negative and A_slow amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and A_slow amplitude negative'
                                    if max_model < amp_thresh:
                                        warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude negative'

                            else:
                                if A_fast > 2000:
                                    if A_slow > 2000:
                                        warning = 'tau values are both negative and both amplitudes are too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold and both amplitudes are too high'
                                            if max_model < amp_thresh:
                                                warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes are too high'

                                    else:
                                        warning = 'tau values are both negative and A_fast amplitude are too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold and A_fast amplitude are too high'
                                            if max_model < amp_thresh:
                                                warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude are too high'
                                else:
                                    if A_slow > 2000:
                                        warning = 'tau values are both negative and A_slow amplitude too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold and A_slow amplitude too high'
                                            if max_model < amp_thresh:
                                                warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude too high'
                                    else:
                                        warning = 'tau values are both negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold'
                                            if max_model < amp_thresh:
                                                warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low'
                else:
                    if A_fast < 0:
                        if A_slow < 0:
                            warning = 'tau_slow negative and both amplitudes are negative'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and both amplitudes are negative'
                                if max_model <= amp_thresh:
                                    warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes are negative'
                        else:
                            warning = 'tau_slow negative and A_fast amplitude negative'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and A_fast amplitude negative'
                                if max_model <= amp_thresh:
                                    warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude negative'
                    else:
                        if A_slow < 0:
                            warning = 'tau_slow negative and A_slow amplitude negative'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and A_slow amplitude negative'
                                if max_model <= amp_thresh:
                                    warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude negative'
                        else:
                            if A_fast > 2000:
                                if A_slow > 2000:
                                    warning = 'tau_slow negative and both amplitudes too high'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and both amplitudes too high'
                                        if max_model <= amp_thresh:
                                            warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes too high'
                                else:
                                    warning = 'tau_slow negative and A_fast amplitude too high'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and A_fast amplitude too high'
                                        if max_model <= amp_thresh:
                                            warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude too high'
                            else:
                                if A_slow > 2000:
                                    warning = 'tau_slow negative and A_slow amplitude too high'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and A_slow amplitude too high'
                                        if max_model <= amp_thresh:
                                            warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude too high'
                                else:
                                    warning = 'tau_slow negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold'
                                        if max_model <= amp_thresh:
                                            warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low'

        else:
            if tau_fast > 0 and tau_slow > 0:
                if tau_fast * 1e-3 <= sweep_length:
                    if tau_slow * 1e-3 <= sweep_length:
                        if max_model >= amp_thresh:
                            if rsquare >= rsq_thresh:
                                if A_fast > 0:
                                    if A_slow > 0:
                                        warning = 'Both amplitudes are positive'
                                    else:
                                        warning = 'A_fast amplitude positive'
                                else:
                                    if A_slow > 0:
                                        warning = 'A_slow amplitude positive'
                                    else:
                                        if A_fast < -10000:
                                            if A_slow < -10000:
                                                warning = 'Both amplitudes far too negative'
                                            else:
                                                warning = 'A_fast amplitude far too negative'
                                        else:
                                            if A_slow < -10000:
                                                warning = 'A_slow amplitude far too negative'
                            else:
                                if A_fast > 0:
                                    if A_slow > 0:
                                        warning = 'Rsquare less than the supplied threshold and both amplitudes negative'
                                    else:
                                        warning = 'Rsquare less than the supplied threshold and A_fast amplitude positive'
                                else:
                                    if A_slow > 0:
                                        warning = 'Rsquare less than the supplied threshold and A_slow amplitude positive'
                                    else:
                                        if A_fast < -10000:
                                            if A_slow < -10000:
                                                warning = 'Rsquare less than the supplied threshold and both amplitudes far too negative'
                                            else:
                                                warning = 'Rsquare less than the supplied threshold and A_fast amplitude far too negative'
                                        else:
                                            if A_slow < -10000:
                                                warning = 'Rsquare less than the supplied threshold and A_slow amplitude far too negative'
                                            else:
                                                warning = 'Rsquare less than the supplied threshold'
                        else:
                            if A_fast > 0:
                                if A_slow > 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both amplitudes negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both amplitudes negative'
                                else:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and A_fast amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and A_fast amplitude positive'
                            else:
                                if A_slow > 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and A_slow amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and A_slow amplitude positive'
                                else:
                                    if A_fast < -10000:
                                        if A_slow < -10000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both amplitudes far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both amplitudes far too negative'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and A_fast amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and A_fast amplitude far too negative'
                                    else:
                                        if A_slow < -10000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and A_slow amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and A_slow amplitude far too negative'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor'
                    else:
                        if max_model >= amp_thresh:
                            if A_fast > 0:
                                if A_slow > 0:
                                    warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes neagtive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes neagtive'
                                else:
                                    warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude positive'
                            else:
                                if A_slow > 0:
                                    warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude positive'
                                else:
                                    if A_fast < -10000:
                                        if A_slow < -10000:
                                            warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes far too negative'
                                        else:
                                            warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude far too negative'
                                    else:
                                        if A_slow < -10000:
                                            warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude far too negative'
                                        else:
                                            warning = 'The tau_slow parameter has taken on a value longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration'
                        else:
                            if A_fast > 0:
                                if A_slow > 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes are positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes are positive'
                                else:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude positive'
                            else:
                                if A_slow > 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude positive'
                                else:
                                    if A_fast < -10000:
                                        if A_slow < -10000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes far too negative'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude far too negative'
                                    else:
                                        if A_slow < -10000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude far too negative'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_slow parameter has taken on a value longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_slow parameter has taken on a value longer than the sweep duration'
                else:
                    if tau_slow * 1e-3 > sweep_length:
                        if max_model >= amp_thresh:
                            if A_fast > 0:
                                if A_slow > 0:
                                    warning = 'Both tau parameters have taken on values longer than the sweep duration and both amplitudes negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes negative'

                                else:
                                    warning = 'Both tau parameters have taken on values longer than the sweep duration and A_fast amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude positive'

                            else:
                                if A_slow > 0:
                                    warning = 'Both tau parameters have taken on values longer than the sweep duration and A_slow amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude positive'
                                else:
                                    if A_fast < -10000:
                                        if A_slow < -10000:
                                            warning = 'Both tau parameters have taken on values longer than the sweep duration and both amplitudes far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes far too negative'

                                        else:
                                            warning = 'Both tau parameters have taken on values longer than the sweep duration and A_fast amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude far too negative'

                                    else:
                                        if A_slow < -10000:
                                            warning = 'Both tau parameters have taken on values longer than the sweep duration and A_slow amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude far too negative'
                                        else:
                                            warning = 'Both tau parameters have taken on values longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration'
                        else:
                            if A_fast > 0:
                                if A_slow > 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and both amplitudes negative'

                                else:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude positive'
                            else:
                                if A_slow > 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude positive'
                                else:
                                    if A_fast < -10000:
                                        if A_slow < -10000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and both amplitudes too hogh'

                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude to high'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude far too negative'
                                    else:
                                        if A_slow < -10000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude far too negative'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and both tau parameters have taken on values longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and both tau parameters have taken on values longer than the sweep duration'
                    else:
                        if max_model >= amp_thresh:
                            if A_fast > 0:
                                if A_slow > 0:
                                    warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes negative'

                                else:
                                    warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude positive'

                            else:
                                if A_slow > 0:
                                    warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude positive'

                                else:
                                    if A_fast < -10000:
                                        if A_slow < -10000:
                                            warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes far too negative'
                                        else:
                                            warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude far too negative'
                                    else:
                                        if A_slow < -10000:
                                            warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude far too negative'
                                        else:
                                            warning = 'The tau_fast parameter has taken on a value longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration'
                        else:
                            if A_fast > 0:
                                if A_slow > 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes negative'
                                else:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude positive'
                            else:
                                if A_slow > 0:
                                    warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude positive'
                                    if rsquare < rsq_thresh:
                                        warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude positive'
                                else:
                                    if A_fast < -10000:
                                        if A_slow < -10000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes far too negative'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude far too negative'
                                    else:
                                        if A_slow < -10000:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude far too negative'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude far too negative'
                                        else:
                                            warning = 'Maximum current amplitude less than the appropriate amplitude threshold and the tau_fast parameter has taken on a value longer than the sweep duration'
                                            if rsquare < rsq_thresh:
                                                warning = 'Maximum current amplitude less than the appropriate amplitude threshold and Rsquare poor and the tau_fast parameter has taken on a value longer than the sweep duration'
            else:
                if tau_fast < 0:
                    if tau_slow > 0:
                        if A_fast > 0:
                            if A_slow > 0:
                                warning = 'tau_fast negative and both amplitudes negative'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold and both amplitudes negative'
                                    if max_model <= amp_thresh:
                                        warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes negative'

                            else:
                                warning = 'tau_fast negative and A_fast amplitude positive'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold and A_fast amplitude positive'
                                    if max_model <= amp_thresh:
                                        warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude positive'
                        else:
                            if A_slow > 0:
                                warning = 'tau_fast negative and A_slow amplitude positive'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold and A_slow amplitude positive'
                                    if max_model <= amp_thresh:
                                        warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude positive'
                            else:
                                if A_fast < -10000:
                                    if A_slow < -10000:
                                        warning = 'tau_fast negative and both amplitudes far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and both amplitudes far too negative'
                                            if max_model <= amp_thresh:
                                                warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes far too negative'

                                    else:
                                        warning = 'tau_fast negative and A_fast amplitude far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and A_fast amplitude far too negative'
                                            if max_model <= amp_thresh:
                                                warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude far too negative'
                                else:
                                    if A_slow < -10000:
                                        warning = 'tau_fast negative and A_slow amplitude far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and A_slow amplitude far too negative'
                                            if max_model <= amp_thresh:
                                                warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude far too negative'
                                    else:
                                        warning = 'tau_fast negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold'
                                            if max_model <= amp_thresh:
                                                warning = 'tau_fast negative, Rsquare below supplied threshold and max current amplitude too low'
                    else:
                        if A_fast > 0:
                            if A_slow > 0:
                                warning = 'tau values are both negative and both amplitudes are positive'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and both amplitudes are positive'
                                    if max_model < amp_thresh:
                                        warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes are positive'

                            else:
                                warning = 'tau values are both negative and A_fast amplitude positive'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and A_fast amplitude positive'
                                    if max_model < amp_thresh:
                                        warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude positive'

                        else:
                            if A_slow > 0:
                                warning = 'tau values are both negative and A_slow amplitude positive'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and A_slow amplitude positive'
                                    if max_model < amp_thresh:
                                        warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude positive'

                            else:
                                if A_fast < -10000:
                                    if A_slow < -10000:
                                        warning = 'tau values are both negative and both amplitudes are too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold and both amplitudes are too high'
                                            if max_model < amp_thresh:
                                                warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes are too high'

                                    else:
                                        warning = 'tau values are both negative and A_fast amplitude are too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold and A_fast amplitude are too high'
                                            if max_model < amp_thresh:
                                                warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude are too high'
                                else:
                                    if A_slow < -10000:
                                        warning = 'tau values are both negative and A_slow amplitude far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold and A_slow amplitude far too negative'
                                            if max_model < amp_thresh:
                                                warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude far too negative'
                                    else:
                                        warning = 'tau values are both negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold'
                                            if max_model < amp_thresh:
                                                warning = 'both tau values are negative, Rsquare below supplied threshold and max current amplitude too low'
                else:
                    if A_fast > 0:
                        if A_slow > 0:
                            warning = 'tau_slow negative and both amplitudes are positive'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and both amplitudes are positive'
                                if max_model <= amp_thresh:
                                    warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes are positive'
                        else:
                            warning = 'tau_slow negative and A_fast amplitude positive'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and A_fast amplitude positive'
                                if max_model <= amp_thresh:
                                    warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude positive'
                    else:
                        if A_slow > 0:
                            warning = 'tau_slow negative and A_slow amplitude positive'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and A_slow amplitude positive'
                                if max_model <= amp_thresh:
                                    warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude positive'
                        else:
                            if A_fast < -10000:
                                if A_slow < -10000:
                                    warning = 'tau_slow negative and both amplitudes far too negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and both amplitudes far too negative'
                                        if max_model <= amp_thresh:
                                            warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and both amplitudes far too negative'
                                else:
                                    warning = 'tau_slow negative and A_fast amplitude far too negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and A_fast amplitude far too negative'
                                        if max_model <= amp_thresh:
                                            warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and A_fast amplitude far too negative'
                            else:
                                if A_slow < -10000:
                                    warning = 'tau_slow negative and A_slow amplitude far too negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and A_slow amplitude far too negative'
                                        if max_model <= amp_thresh:
                                            warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low and A_slow amplitude far too negative'
                                else:
                                    warning = 'tau_slow negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold'
                                        if max_model <= amp_thresh:
                                            warning = 'tau_slow negative, Rsquare below supplied threshold and max current amplitude too low'

    else:
    # Warnings for the normal sweeps
        #if actual_sweep < 11:
        if sweep_voltage > -80:
            if tau_fast > 0 and tau_slow > 0:
                if tau_fast*1e-3 > sweep_length:
                    if tau_slow*1e-3 > sweep_length:
                        if A_fast < 0:
                            if A_slow < 0:
                                warning = 'Both tau parameters have taken on values longer than the sweep duration and both amplitudes negative'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes negative'

                            else:
                                warning = 'Both tau parameters have taken on values longer than the sweep duration and A_fast amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude negative'
                        else:
                            if A_slow < 0:
                                warning = 'Both tau parameters have taken on values longer than the sweep duration and A_slow amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude negative'

                            else:
                                if A_fast > 2000:
                                    if A_slow > 2000:
                                        warning = 'Both tau parameters have taken on values longer than the sweep duration and both amplitudes too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes too high'

                                    else:
                                        warning = 'Both tau parameters have taken on values longer than the sweep duration and A_fast amplitude too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude too high'

                                else:
                                    if A_slow > 2000:
                                        warning = 'Both tau parameters have taken on values longer than the sweep duration and A_slow parameter too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_slow parameter too high'

                                    else:
                                        warning = 'Both tau parameters have taken on values longer than the sweep duration'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration'
                    else:
                        if A_fast < 0:
                            if A_slow < 0:
                                warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes negative'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes negative'

                            else:
                                warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'

                        else:
                            if A_slow < 0:
                                warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'

                            else:
                                if A_fast > 2000:
                                    if A_slow > 2000:
                                        warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes too high'

                                    else:
                                        warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast parameter too high'

                                else:
                                    if A_slow > 2000:
                                        warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'

                                    else:
                                        warning = 'The tau_fast parameter has taken on a value longer than the sweep duration'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration'
                else:
                    if tau_slow*1e-3 > sweep_length:
                        if A_fast < 0:
                            if A_slow < 0:
                                warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes negative'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes negative'
                            else:
                                warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude negative'
                        else:
                            if A_slow < 0:
                                warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude negative'
                            else:
                                if A_fast > 2000:
                                    if A_slow > 2000:
                                        warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both amplitudes too high'
                                    else:
                                        warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast amplitude too high'
                                else:
                                    if A_slow > 2000:
                                        warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow amplitude too high'
                                    else:
                                        warning = 'The tau_slow parameter has taken on a value longer than the sweep duration'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration'
                    else:
                        if rsquare < rsq_thresh:
                            if A_fast < 0:
                                if A_slow < 0:
                                    warning = 'Rsquare less than the supplied threshold and both amplitudes negative'
                                else:
                                    warning = 'Rsquare less than the supplied threshold and A_fast amplitude negative'
                            else:
                                if A_slow < 0:
                                    warning = 'Rsquare less than the supplied threshold and A_slow amplitude negative'
                                else:
                                    if A_fast > 2000:
                                        if A_slow > 2000:
                                            warning = 'Rsquare less than the supplied threshold and both amplitudes too high'
                                        else:
                                            warning = 'Rsquare less than the supplied threshold and A_fast amplitude too high'
                                    else:
                                        if A_slow > 2000:
                                            warning = 'Rsquare less than the supplied threshold and A_slow amplitude too high'
                                        else:
                                            warning = 'Rsquare less than the supplied threshold'
                        else:
                            if A_fast < 0:
                                if A_slow < 0:
                                    warning = 'Both amplitudes negative'
                                else:
                                    warning = 'A_fast amplitude negative'
                            else:
                                if A_slow < 0:
                                    warning = 'A_slow amplitude negative'
                                else:
                                    if A_fast > 2000:
                                        if A_slow > 2000:
                                            warning = 'Both amplitudes too high'
                                        else:
                                            warning = 'A_fast amplitude too high'
                                    else:
                                        if A_slow > 2000:
                                            warning = 'A_slow amplitude too high'
            else:
                if tau_fast < 0:
                    if tau_slow > 0:
                        if A_fast < 0:
                            if A_slow < 0:
                                warning = 'tau_fast negative and both amplitudes negative'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold and both amplitudes negative'
                            else:
                                warning = 'tau_fast negative and A_fast amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold and A_fast amplitude negative'
                        else:
                            if A_slow < 0:
                                warning = 'tau_fast negative and A_slow amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold and A_slow amplitude negative'
                            else:
                                if A_fast > 2000:
                                    if A_slow > 2000:
                                        warning = 'tau_fast negative and both amplitudes too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and both amplitudes too high'
                                    else:
                                        warning = 'tau_fast negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and A_fast amplitude too high'
                                else:
                                    if A_slow > 2000:
                                        warning = 'tau_fast negative and A_slow amplitude too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and A_slow amplitude too high'
                                    else:
                                        warning = 'tau_fast negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold'
                    else:
                        if A_fast < 0:
                            if A_slow < 0:
                                warning = 'tau values are both negative and both amplitudes negative'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and both amplitudes negativ'
                            else:
                                warning = 'tau values are both negative and A_fast amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and A_fast amplitude negative'
                        else:
                            if A_slow < 0:
                                warning = 'tau values are both negative and A_slow amplitude negative'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and A_slow amplitude negative'
                            else:
                                if A_fast > 2000:
                                    if A_slow > 2000:
                                        warning = 'tau values are both negative and both amplitudes too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold and both amplitudes too high'
                                    else:
                                        warning = 'tau values are both negative and A_fast amplitude too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold A_fast amplitude too high'
                                else:
                                    if A_slow > 2000:
                                        warning = 'tau values are both negative and A_slow amplitude too high'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold A_slow amplitude too high'
                                    else:
                                        warning = 'tau values are both negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold'
                else:
                    if A_fast < 0:
                        if A_slow < 0:
                            warning = 'tau_slow negative and both amplitudes negative'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and both amplitudes negative'
                        else:
                            warning = 'tau_slow negative and A_fast amplitude negative'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and A_fast amplitude negative'
                    else:
                        if A_slow < 0:
                            warning = 'tau_slow negative and A_slow amplitude negative'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and A_slow amplitude negative'
                        else:
                            if A_fast > 2000:
                                if A_slow > 2000:
                                    warning = 'tau_slow negative and both amplitudes too high'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and both amplitudes too high'
                                else:
                                    warning = 'tau_slow negative and A_fast amplitude too high'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and A_fast amplitude too high'
                            else:
                                if A_slow > 2000:
                                    warning = 'tau_slow negative and A_slow amplitude too high'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and A_slow amplitude too high'
                                else:
                                    warning = 'tau_slow negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold'
        else:
        #Warning analysis for negative voltage sweeps
            if tau_fast > 0 and tau_slow > 0:
                if tau_fast * 1e-3 > sweep_length:
                    if tau_slow * 1e-3 > sweep_length:
                        if A_fast > 0:
                            if A_slow > 0:
                                warning = 'Both tau parameters have taken on values longer than the sweep duration and both amplitudes are positive'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes are positive'
                            else:
                                warning = 'Both tau parameters have taken on values longer than the sweep duration and A_fast amplitude is positive'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude is positive'
                        else:
                            if A_slow > 0:
                                warning = 'Both tau parameters have taken on values longer than the sweep duration and A_slow amplitude is positive'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude is positive'
                            else:
                                if A_fast < -10000:
                                    if A_slow < -10000:
                                        warning = 'Both tau parameters have taken on values longer than the sweep duration and both amplitudes are far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and both amplitudes are far too negative'
                                    else:
                                        warning = 'Both tau parameters have taken on values longer than the sweep duration and A_fast amplitude far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_fast amplitude far too negative'
                                else:
                                    if A_slow < -10000:
                                        warning = 'Both tau parameters have taken on values longer than the sweep duration and A_slow amplitude far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration and A_slow amplitude far too negative'
                                    else:
                                        warning = 'Both tau parameters have taken on values longer than the sweep duration'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and both tau parameters have taken on values longer than the sweep duration'
                    else:
                        if A_fast > 0:
                            if A_slow > 0:
                                warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes are positive'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitudes are positive'
                            else:
                                warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude is positive'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude is positive'
                        else:
                            if A_slow > 0:
                                warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude is positive'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude is positive'
                            else:
                                if A_fast < -10000:
                                    if A_slow < -10000:
                                        warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and both amplitude far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and both amplitude far too negative'
                                    else:
                                        warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_fast amplitude far too negative'
                                else:
                                    if A_slow < -10000:
                                        warning = 'The tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration and A_slow amplitude far too negative'
                                    else:
                                        warning = 'The tau_fast parameter has taken on a value longer than the sweep duration'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_fast parameter has taken on a value longer than the sweep duration'
                else:
                    if tau_slow * 1e-3 > sweep_length:
                        if A_fast > 0:
                            if A_slow > 0:
                                warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and both parameters are positive'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both parameters are positive'
                            else:
                                warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_fast parameter is positive'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast parameter is positive'
                        else:
                            if A_slow > 0:
                                warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_slow parameter is positive'
                                if rsquare < rsq_thresh:
                                    warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow parameter is positive'
                            else:
                                if A_fast < -10000:
                                    if A_slow < -10000:
                                        warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and both parameters are far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and both parameters are far too negative'
                                    else:
                                        warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_fast parameter is far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_fast parameter is far too negative'
                                else:
                                    if A_slow < -10000:
                                        warning = 'The tau_slow parameter has taken on a value longer than the sweep duration and A_slow parameter is far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration and A_slow parameter is far too negative'
                                    else:
                                        warning = 'The tau_slow parameter has taken on a value longer than the sweep duration'
                                        if rsquare < rsq_thresh:
                                            warning = 'Rsquare less than the supplied threshold and the tau_slow parameter has taken on a value longer than the sweep duration'
                    else:
                        if rsquare < rsq_thresh:
                            if A_fast > 0:
                                if A_slow > 0:
                                    warning = 'Rsquare less than the supplied threshold and both amplitudes are positive'
                                else:
                                    warning = 'Rsquare less than the supplied threshold and A_fast amplitude is positive'
                            else:
                                if A_slow > 0:
                                    warning = 'Rsquare less than the supplied threshold and A_slow amplitude is positive'
                                else:
                                    if A_fast < -10000:
                                        if A_slow < -10000:
                                            warning = 'Rsquare less than the supplied threshold and both amplitudes are far too negative'
                                        else:
                                            warning = 'Rsquare less than the supplied threshold and A_fast amplitude is far too negative'
                                    else:
                                        if A_slow < -10000:
                                            warning = 'Rsquare less than the supplied threshold and A_slow amplitude is far too negative'
                                        else:
                                            warning = 'Rsquare less than the supplied threshold'
                        else:
                            if A_fast > 0:
                                if A_slow > 0:
                                    warning = 'Both amplitudes are positive'
                                else:
                                    warning = 'A_fast amplitude is positive'
                            else:
                                if A_slow > 0:
                                    warning = 'A_slow amplitude is positive'
                                else:
                                    if A_fast < -10000:
                                        if A_slow < -10000:
                                            warning = 'Both amplitudes are far too negative'
                                        else:
                                            warning = 'A_fast amplitude is far too negative'
                                    else:
                                        if A_slow < -10000:
                                            warning = 'A_slow amplitude is far too negative'
            else:
                if tau_fast < 0:
                    if tau_slow > 0:
                        if A_fast > 0:
                            if A_slow > 0:
                                warning = 'tau_fast negative and both amplitudes are positive'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold and both amplitudes are positive'
                            else:
                                warning = 'tau_fast negative and A_fast amplitude is positive'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold A_fast amplitude is positive'
                        else:
                            if A_slow > 0:
                                warning = 'tau_fast negative A_slow amplitude is positive'
                                if rsquare < rsq_thresh:
                                    warning = 'tau_fast negative and Rsquare below supplied threshold A_slow amplitude is positive'
                            else:
                                if A_fast < -10000:
                                    if A_slow < -10000:
                                        warning = 'tau_fast negative and both amplitudes are far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and both amplitudes are far too negative'
                                    else:
                                        warning = 'tau_fast negative and A_fast amplitude is far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and A_fast amplitude is far too negative'
                                else:
                                    if A_slow < -10000:
                                        warning = 'tau_fast negative and A_slow amplitude is far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold and A_slow amplitude is far too negative'
                                    else:
                                        warning = 'tau_fast negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'tau_fast negative and Rsquare below supplied threshold'
                    else:
                        if A_fast > 0:
                            if A_slow > 0:
                                warning = 'tau values are both negative and both amplitudes are positive'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and both amplitudes are positive'
                            else:
                                warning = 'tau values are both negative and A_fast amplitude is positive'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and A_fast amplitude is positive'
                        else:
                            if A_slow > 0:
                                warning = 'tau values are both negative and A_slow amplitude is positive'
                                if rsquare < rsq_thresh:
                                    warning = 'both tau values are negative and Rsquare below supplied threshold and A_slow amplitude is positive'
                            else:
                                if A_fast < -10000:
                                    if A_slow < -10000:
                                        warning = 'tau values are both negative and both amplitudes are far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold and both amplitudes are far too negative'
                                    else:
                                        warning = 'tau values are both negative and A_fast amplitude far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold and A_fast amplitude far too negative'
                                else:
                                    if A_slow < -10000:
                                        warning = 'tau values are both negative and A_slow amplitude far too negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold and A_slow amplitude far too negative'
                                    else:
                                        warning = 'tau values are both negative'
                                        if rsquare < rsq_thresh:
                                            warning = 'both tau values are negative and Rsquare below supplied threshold'
                else:
                    if A_fast > 0:
                        if A_slow > 0:
                            warning = 'tau_slow negative and both amplitudes are positive'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and both amplitudes are positive'
                        else:
                            warning = 'tau_slow negative and A_fast amplitude is positive'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and A_fast amplitude is positive'
                    else:
                        if A_slow > 0:
                            warning = 'tau_slow negative and A_slow amplitude is positive'
                            if rsquare < rsq_thresh:
                                warning = 'tau_slow negative and Rsquare below supplied threshold and A_slow amplitude is positive'
                        else:
                            if A_fast < -10000:
                                if A_slow < -10000:
                                    warning = 'tau_slow negative and both amplitudes are far too negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and both amplitudes are far too negative'
                                else:
                                    warning = 'tau_slow negative and A_fast amplitude is far too negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and A_fast amplitude is far too negative'
                            else:
                                if A_slow < -10000:
                                    warning = 'tau_slow negative and A_slow amplitude is far too negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold and A_slow amplitude is far too negative'
                                else:
                                    warning = 'tau_slow negative'
                                    if rsquare < rsq_thresh:
                                        warning = 'tau_slow negative and Rsquare below supplied threshold'

    return warning
