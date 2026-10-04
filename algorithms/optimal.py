def optimal_page_replacement(reference_string, frame_count):
    frames = []
    frame_history = []
    status = []

    page_faults = 0
    page_hits = 0

    for i in range(len(reference_string)):
        page = reference_string[i]

        if page in frames:
            status.append("Hit")
            page_hits += 1

        else:
            status.append("Fault")
            page_faults += 1

            if len(frames) < frame_count:
                frames.append(page)

            else:
                future = reference_string[i + 1:]

                farthest_index = -1
                page_to_replace = None

                for frame_page in frames:

                    if frame_page not in future:
                        page_to_replace = frame_page
                        break

                    next_use = future.index(frame_page)

                    if next_use > farthest_index:
                        farthest_index = next_use
                        page_to_replace = frame_page

                frames[frames.index(page_to_replace)] = page

        frame_history.append(frames.copy())

    return {
        "frame_history": frame_history,
        "status": status,
        "page_faults": page_faults,
        "page_hits": page_hits
    }
