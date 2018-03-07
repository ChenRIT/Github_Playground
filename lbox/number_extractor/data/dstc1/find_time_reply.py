import os

import jsonpickle
import csv

label_suffix = 'labels.json'

def find_time_exps(label_fname):
    """ 
    Find all user replies that mention time

    @return: a list of records that contain (reply, time)

    """
    #print("Processing: {}".format(label_fname))
    labels = None
    with open(label_fname) as label_file:
        labels = jsonpickle.decode(label_file.read())

    #print(logs['turns'][0]['output']['transcript'])

    # Find user reply turns where "time.hour" is correctly labeled
    # Record the user replay transcript and the labeled value
    time_records = []
    for turn in labels['turns']:
        label_list = None
        if 'slu-labels' in turn:
            label_list = turn['slu-labels']
        else:
            continue

        transcription = None
        if 'transcription' in turn:
            transcription = turn['transcription']
        else:
            continue
        
        for label in label_list:
            has_time = False
            time_hour = "-"
            time_minute = "-"
            
            if "time.hour" in label['slots'] and label['label']:
                time_hour = label['slots']['time.hour']
                has_time = True

            if "time.minute" in label['slots'] and label['label']:
                time_minute = label['slots']['time.minute']
                has_time = True

            if has_time and transcription != "yes":
                time_records.append([transcription, time_hour, time_minute])
                break

    return time_records

def fetch_label_fnames(dir):
    """
    Obtain all label file names
    """
    label_fnames = []
    subfiles = os.listdir(dir)
    for fname in subfiles:
        file_path = os.path.join(dir, fname)
        if os.path.isfile(file_path):
            if fname.endswith(label_suffix):
                label_fnames.append(file_path)

        if os.path.isdir(file_path):
            label_fnames += fetch_label_fnames(file_path)
            
    return label_fnames
            

def test():
    # Read input labels
    input_fname = "/Users/chen/Research/Playground/Github_Playground/lbox/number_extractor/data/dstc1/DSTC_1/20090913/046/dstc.labels.json"
    print(find_time_exps(input_fname))

if __name__ == "__main__":
    # Run through DSTC_1 files
    head_dir = "/Users/chen/Research/Playground/Github_Playground/lbox/number_extractor/data/dstc1"
    #head_dir = "/Users/chen/Research/Playground/Github_Playground/lbox/number_extractor/data/dstc1/test"
    # head_dir = "/Users/chen/Research/Playground/Github_Playground/lbox/number_extractor/data/dstc1/DSTC_1"

    output_fname = "time_replies.csv"
    label_files = fetch_label_fnames(head_dir)

    time_records = []
    for lb_file in label_files:
        time_records += find_time_exps(lb_file)

    with open(output_fname, 'w') as ofile:
        datawriter = csv.writer(ofile)
        datawriter.writerow(['index', 'sentence', 'Hour', 'Minute'])
        for i in range(len(time_records)):
            idx_record = [i] + time_records[i]
            datawriter.writerow(idx_record)

            

