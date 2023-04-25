from flask import Blueprint, render_template
from flask_login import login_required, current_user

video = Blueprint('video', __name__)


@video.route('/video-data')
@login_required
def analytics_data():
    pass


@video.route('/video_feed', methods=['GET'])
@login_required
def video_feed():
    start = time.time_ns()
    frame_count = 0
    actual_frame_count = 0
    saved_items = []
    global is_record_clip
    frame_folder = "{}/{}".format(RECORDS_FOLDER, clip_id)
    frame_file_name = "{}/frame_{}_{}.jpg"
    if not os.path.exists(frame_folder):
        os.mkdir(frame_folder)
    saved_boxes = []
    num_stationary = 0
    avg_speed = 0
    while True:
        _, frame = capture.read()
        if frame is None:
            print("End of stream")
            break

        if playonly == 0:
            inputImage = format_yolov5(frame)
            outs = detect(inputImage, net)

            class_ids, confidences, boxes = wrap_detection(inputImage, outs[0])
            distances = []
            sub_distance = []
            for i in range(len(boxes)):
                sub_distance.append(10000)
            for i in range(len(boxes)):
                distances.append(sub_distance.copy())
            for i in range(len(boxes)):
                sub_distance = []
                for k in range(len(boxes)):
                    sub_distance.append(10000)
                for j in range(len(boxes)):
                    if i != j:
                        distances[i][j] = dist.euclidean(boxes[i], boxes[j])

            nearMiss = []
            for i in range(len(boxes)):
                nearMiss.append(0)
            for i in range(len(boxes)):
                m = min(distances[i])
                idx = distances[i].index(m)
                if m < 89:
                    nearMiss[idx] = 1
                else:
                    nearMiss[i] = 0

            frame_count += 1
            for vehicle in class_list:
                sess[vehicle] = 0
            #   my_analytics_data[vehicle] =

            speed_sum = 0
            speed_count = 0

            for (classid, confidence, box, j) in zip(class_ids, confidences, boxes, range(len(boxes))):
                color = colors[int(classid) % len(colors)]
                sess[class_list[classid]] = sess[class_list[classid]] + 1
                box_center_x = (box[0] + box[2]) / 2
                box_center_y = (box[1] + box[3]) / 2

                shortest_dis = 5
                current_id = -1
                speed = 0
                for idx, si in enumerate(saved_items):
                    dis = dist.euclidean([box_center_x, box_center_y], [si['x'], si['y']])
                    if shortest_dis > dis:
                        speed = (dis * 30) * 60 * 60 / 10000
                        current_id = idx
                        break
                if current_id == -1:
                    saved_items.append({
                        'x': box_center_x,
                        'y': box_center_y,
                        'speed': speed
                    })
                    current_id = len(saved_items) - 1;
                else:
                    saved_items[current_id] = {
                        'x': box_center_x,
                        'y': box_center_y,
                        'speed': speed
                    }
                if speed != 0:
                    speed_sum += speed
                    speed_count += 1

                if nearMiss[j] == 1:
                    color = (165, 85, 236)
                cv2.rectangle(frame, box, color, 2)
                cv2.rectangle(frame, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)
                cv2.putText(frame, "{} - {}".format(class_list[classid], current_id), (box[0], box[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0))

            if frame_count >= 30:
                frame_count = 0
            avg_speed = speed_sum / speed_count if speed_count > 0 else 1
            incident_prob = round(sum(nearMiss) * 100 / (len(nearMiss) + 1))
            accident_prob = round(incident_prob / 10)

            sess['incident_prob'] = incident_prob
            sess['accident_prob'] = accident_prob
            sess['avg_speed'] = avg_speed
            sess['stationary_object'] = len(boxes) - speed_count

            actual_frame_count = actual_frame_count + 1
            if is_record_clip:
                ffn = frame_file_name.format(frame_folder, clip_id, actual_frame_count)
                cv2.imwrite(ffn, frame)

        ret1, buffer1 = cv2.imencode('.jpg', frame)
        myFrame = buffer1.tobytes()
        try:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + myFrame + b'\r\n')
        except GeneratorExit:
            is_record_clip = False
            return


@video.route('/start-record-clip')
def start_record_clip():
    pass


@video.route('/stop-record-clip')
def stop_record_clip():
    pass


@video.route('/is-recording')
def is_video_recoding():
    file = pass


@video.route('/create-clip', methods=['POST'])
def create_video():
    pass


@video.route('/check-camera', methods=['GET'])
def check_camera():
    pass
