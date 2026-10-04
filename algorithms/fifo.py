def fifo_page_replacement(reference_string, frame_count):
    frames = []
    frame_history = []
    status = []

    page_faults = 0
    page_hits = 0
    pointer = 0

    for page in reference_string:

        if page in frames:
            status.append("Hit")
            page_hits += 1

        else:
            status.append("Fault")
            page_faults += 1

            if len(frames) < frame_count:
                frames.append(page)

            else:
                frames[pointer] = page
                pointer = (pointer + 1) % frame_count

        frame_history.append(frames.copy())

    return {
        "frame_history": frame_history,
        "status": status,
        "page_faults": page_faults,
        "page_hits": page_hits
    }
