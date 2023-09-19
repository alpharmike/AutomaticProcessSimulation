import argparse
import os
from pathlib import Path

import simulation_activity
import pm4py


def discover_model_from_log(log):
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)
    return net, initial_marking, final_marking


def read_orig_sim_file_path():
    """
        Reads the input file path from the Command Line Interface and verifies if the file exists
        Returns
        --------------
        file.file_path
                The file path of the input event log file
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("orig_file_path", type=Path)
    parser.add_argument("sim_file_path", type=Path)
    args = parser.parse_args()
    orig_file = args.orig_file_path
    sim_file = args.sim_file_path
    print("File received: ", orig_file)
    print("File received: ", sim_file)
    if not orig_file.exists():
        print("original event log file does not exist. Please input correct file")
        exit()
    if not sim_file.exists():
        print("simulated event log file does not exist. Please input correct file")
        exit()

    return str(orig_file), str(sim_file)


def verify_extension_and_import(file_path):
    """
            This function verifies that the extension of the event log file is .xes or .csv and imports the
            logs from those files
            Returns
            --------------
            log
                The input event logs in the form of a log
            """

    # file_path ="Prozessmodel.xes"
    file_name, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.replace("'))", "")
    print("File Extension: ", file_extension)
    if file_extension == ".xes":
        log = simulation_activity.import_xes(file_path)
        return log
    elif file_extension == ".csv":
        log = simulation_activity.import_csv(file_path)
        return log
    else:
        print("Unsupported extension. Supported file extensions are .xes and .csv ONLY")
        exit()


if __name__ == '__main__':
    orig_file_path, sim_file_path = read_orig_sim_file_path()
    orig_log = verify_extension_and_import(orig_file_path)
    sim_log = verify_extension_and_import(sim_file_path)
    orig_net, orig_im, orig_fm = discover_model_from_log(orig_log)
    sim_net, sim_im, sim_fm = discover_model_from_log(sim_log)

    pm4py.save_vis_petri_net(orig_net, orig_im, orig_fm, "orig_net.png")
    pm4py.save_vis_petri_net(sim_net, sim_im, sim_fm, "sim_petri_net.png")

