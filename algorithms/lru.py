def lru_page_replacement(reference_string, frame_count):
    frames = []
    frame_history = []
    status = []

    page_faults = 0
    page_hits = 0

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
                least_recently_used = None
                least_recent_index = -1

                for i in range(len(frames)):
                    page_index = -1

                    for j in range(len(reference_string)):
                        if reference_string[j] == frames[i]:
                            page_index = j

                    if page_index < least_recent_index or least_recent_index == -1:
                        least_recent_index = page_index
                        least_recently_used = frames[i]

                frames[frames.index(least_recently_used)] = page

        frame_history.append(frames.copy())

    return {
        "frame_history": frame_history,
        "status": status,
        "page_faults": page_faults,
        "page_hits": page_hits
    }
