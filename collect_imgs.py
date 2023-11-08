import os
import cv2


DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

#print(*[chr(i).upper() for i in range(ord("a"), ord("z") + 1)], sep="\n")
with open("labels.txt", "r", encoding="UTF-8") as file:
    labels = tuple(label.rstrip() for label in file.readlines())
full_cycle, class_id, class_label = False, -1, str()

capture = cv2.VideoCapture(0)
while True:
    if full_cycle:
        class_id = int(class_id) + 1
        if class_id >= len(labels):
            print("Сбор данных остановлен.")
            break
        class_label = labels[class_id]
    else:
        try:
            for i, label in enumerate(labels):
                if i % 10 == 0:
                    print()
                print(f"{str(i).rjust(2, ' ')}: {label}", end="\t\t")
            class_id = int(input("\nВведите номер класса для захвата изображения (-1 — сбор для всех классов; -2 — выход): "))
            if class_id < -2:
                raise IndexError
            elif class_id == -2:
                print("Сбор данных остановлен.")
                break
            elif class_id == -1:
                full_cycle = True
                continue
            else:
                class_label = labels[class_id]
        except ValueError:
            print("Ошибка: введено нечисловое значение!!!")
            continue
        except IndexError:
            print("Ошибка: введённого класса не существует!!!")
            continue

    if not os.path.exists(os.path.join(DATA_DIR, str(class_id))):
        os.makedirs(os.path.join(DATA_DIR, str(class_id)))

    print(f'Сбор данных для класса {class_id} — жест для "{class_label}"')

    while True:
        _, frame = capture.read()
        message = f'Press "Q" to capture...'

        cv2.putText(frame, message, (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow("Signs capture", frame)
        if cv2.waitKey(25) == ord("q"):
            break

    start = len(os.listdir(os.path.join(DATA_DIR, str(class_id))))
    stop = start + 100
    for counter in range(start, stop):
        _, frame = capture.read()
        cv2.imshow("Signs capture", frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, str(class_id), f"{counter}.jpg"), frame)

capture.release()
cv2.destroyAllWindows()
