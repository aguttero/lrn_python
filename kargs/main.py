

def fetch_agrmnt_by_wkflow(start_date, end_date, *wf_ids):
    print (f"start_date= {start_date}, end_date= {end_date}, wf_ids_type= {type(wf_ids)}, wf_ids= {wf_ids!r}")
    print(f"{wf_ids[0]}")
    pass


def main():
    # RUN YOUR PROCESS
    target_wkflow_list = ["7","8"]
    target_wkflow_tuple = ("1","2")
    target_wkflow_tuple2 = "3","4"
    fetch_agrmnt_by_wkflow("start", "end", target_wkflow_tuple)
    fetch_agrmnt_by_wkflow("start", "end", target_wkflow_tuple2)
    fetch_agrmnt_by_wkflow("start", "end", "5", "6")
    fetch_agrmnt_by_wkflow("start", "end", target_wkflow_list)
    fetch_agrmnt_by_wkflow("start", "end", "9")
    return 0


if __name__ == "__main__":
    exit_code: int = main()
    print (f"exit code: {exit_code}")
    exit(exit_code)