def generate_filename_from_template(templatefname, n_frame_step, n_frame_window):
    start, end = templatefname.split('.')
    return '{}_{}_{}.{}'.format(start, n_frame_step, n_frame_window, end)
