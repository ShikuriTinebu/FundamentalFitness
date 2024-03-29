# -*- coding: utf-8 -*-
"""Rishik Buneti - FundamentalFitness Final Draft.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b1gBo_PHr2cZWw_aqVGTQ-hyVIch9wax

Fundamental Fitness is an AI exercise form correction companion to help users perfect their form in any exercise which they workout with. Our AI uses Google Clouds movenet model to help keep track of 17 points on the user's body to accurately identify and compare their form to that of an expert, as well as help identify what they may need to correct.

# FundamentalFitness AI

## Base Setup
"""

!pip install -q imageio
!pip install -q opencv-python
!pip install -q git+https://github.com/tensorflow/docs
!pip install gTTS
!pip install JavaScript

#Imports (This code was written on google collab, however import files in other code editors as necessary)
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow_docs.vis import embed
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as patches
import imageio
from IPython.display import HTML
import time
import io
import PIL
from IPython.display import display, Javascript, Image, Audio
from base64 import b64decode, b64encode
from google.colab.output import eval_js
import html
from gtts import gTTS
import sys
import os

KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

KEYPOINT_EDGE_INDS_TO_COLOR = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

def _keypoints_and_edges_for_display(keypoints_with_scores,
                                     height,
                                     width,
                                     keypoint_threshold=0.11):
  keypoints_all = []
  keypoint_edges_all = []
  edge_colors = []
  num_instances, _, _, _ = keypoints_with_scores.shape
  for idx in range(num_instances):
    kpts_x = keypoints_with_scores[0, idx, :, 1]
    kpts_y = keypoints_with_scores[0, idx, :, 0]
    kpts_scores = keypoints_with_scores[0, idx, :, 2]
    kpts_absolute_xy = np.stack(
        [width * np.array(kpts_x), height * np.array(kpts_y)], axis=-1)
    kpts_above_thresh_absolute = kpts_absolute_xy[
        kpts_scores > keypoint_threshold, :]
    keypoints_all.append(kpts_above_thresh_absolute)

    for edge_pair, color in KEYPOINT_EDGE_INDS_TO_COLOR.items():
      if (kpts_scores[edge_pair[0]] > keypoint_threshold and
          kpts_scores[edge_pair[1]] > keypoint_threshold):
        x_start = kpts_absolute_xy[edge_pair[0], 0]
        y_start = kpts_absolute_xy[edge_pair[0], 1]
        x_end = kpts_absolute_xy[edge_pair[1], 0]
        y_end = kpts_absolute_xy[edge_pair[1], 1]
        line_seg = np.array([[x_start, y_start], [x_end, y_end]])
        keypoint_edges_all.append(line_seg)
        edge_colors.append(color)
  if keypoints_all:
    keypoints_xy = np.concatenate(keypoints_all, axis=0)
  else:
    keypoints_xy = np.zeros((0, 17, 2))

  if keypoint_edges_all:
    edges_xy = np.stack(keypoint_edges_all, axis=0)
  else:
    edges_xy = np.zeros((0, 2, 2))

  # print(keypoints_xy)
  return keypoints_xy, edges_xy, edge_colors


def draw_prediction_on_image(
    image, keypoints_with_scores, crop_region=None, close_figure=False,
    output_image_height=None):
  height, width, channel = image.shape
  aspect_ratio = float(width) / height
  fig, ax = plt.subplots(figsize=(12 * aspect_ratio, 12))
  # To remove the huge white borders
  fig.tight_layout(pad=0)
  ax.margins(0)
  ax.set_yticklabels([])
  ax.set_xticklabels([])
  plt.axis('off')

  im = ax.imshow(image)
  line_segments = LineCollection([], linewidths=(4), linestyle='solid')
  ax.add_collection(line_segments)
  # Turn off tick labels
  scat = ax.scatter([], [], s=60, color='#FF1493', zorder=3)

  (keypoint_locs, keypoint_edges,
   edge_colors) = _keypoints_and_edges_for_display(
       keypoints_with_scores, height, width)

  line_segments.set_segments(keypoint_edges)
  line_segments.set_color(edge_colors)
  if keypoint_edges.shape[0]:
    line_segments.set_segments(keypoint_edges)
    line_segments.set_color(edge_colors)
  if keypoint_locs.shape[0]:
    scat.set_offsets(keypoint_locs)

  if crop_region is not None:
    xmin = max(crop_region['x_min'] * width, 0.0)
    ymin = max(crop_region['y_min'] * height, 0.0)
    rec_width = min(crop_region['x_max'], 0.99) * width - xmin
    rec_height = min(crop_region['y_max'], 0.99) * height - ymin
    rect = patches.Rectangle(
        (xmin,ymin),rec_width,rec_height,
        linewidth=1,edgecolor='b',facecolor='none')
    ax.add_patch(rect)

  fig.canvas.draw()
  image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
  image_from_plot = image_from_plot.reshape(
      fig.canvas.get_width_height()[::-1] + (3,))
  plt.close(fig)
  if output_image_height is not None:
    output_image_width = int(output_image_height / height * width)
    image_from_plot = cv2.resize(
        image_from_plot, dsize=(output_image_width, output_image_height),
         interpolation=cv2.INTER_CUBIC)
  return image_from_plot

def to_gif(images, duration):
  """Converts image sequence (4D numpy array) to gif."""
  imageio.mimsave('./animation.gif', images, duration=duration)
  return embed.embed_file('./animation.gif')

def progress(value, max=100):
  return HTML("""
      <progress
          value='{value}'
          max='{max}',
          style='width: 100%'
      >
          {value}
      </progress>
  """.format(value=value, max=max))

"""## Load Movenet Model"""

model_name = "movenet_lightning" #@param ["movenet_lightning", "movenet_thunder", "movenet_lightning_f16.tflite", "movenet_thunder_f16.tflite", "movenet_lightning_int8.tflite", "movenet_thunder_int8.tflite"]

if "tflite" in model_name:
  if "movenet_lightning_f16" in model_name:
    !wget -q -O model.tflite https://tfhub.dev/google/lite-model/movenet/singlepose/lightning/tflite/float16/4?lite-format=tflite
    input_size = 192
  elif "movenet_thunder_f16" in model_name:
    !wget -q -O model.tflite https://tfhub.dev/google/lite-model/movenet/singlepose/thunder/tflite/float16/4?lite-format=tflite
    input_size = 256
  elif "movenet_lightning_int8" in model_name:
    !wget -q -O model.tflite https://tfhub.dev/google/lite-model/movenet/singlepose/lightning/tflite/int8/4?lite-format=tflite
    input_size = 192
  elif "movenet_thunder_int8" in model_name:
    !wget -q -O model.tflite https://tfhub.dev/google/lite-model/movenet/singlepose/thunder/tflite/int8/4?lite-format=tflite
    input_size = 256
  else:
    raise ValueError("Unsupported model name: %s" % model_name)

  # Initialize the TFLite interpreter
  interpreter = tf.lite.Interpreter(model_path="model.tflite")
  interpreter.allocate_tensors()

  def movenet(input_image):
    # TF Lite format expects tensor type of uint8.
    input_image = tf.cast(input_image, dtype=tf.uint8)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
    # Invoke inference.
    interpreter.invoke()
    # Get the model prediction.
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
    print(keypoints_with_scores)
    return keypoints_with_scores

else:
  if "movenet_lightning" in model_name:
    module = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
    input_size = 192
  elif "movenet_thunder" in model_name:
    module = hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
    input_size = 256
  else:
    raise ValueError("Unsupported model name: %s" % model_name)

  def movenet(input_image):
    model = module.signatures['serving_default']

    # SavedModel format expects tensor type of int32.
    input_image = tf.cast(input_image, dtype=tf.int32)
    # Run model inference.
    outputs = model(input_image)
    # Output is a [1, 1, 17, 3] tensor.
    keypoints_with_scores = outputs['output_0'].numpy()
    return keypoints_with_scores

"""Run Program With Live Stream (Squats)"""

#Variables Assignment
num_of_faces = 0
num_of_pictures_taken = 0
minutes_running = 3
end_time = time.time() + 60 * minutes_running

# function to convert the JavaScript object into an OpenCV image
def js2img(jsr):
  iwizbyts = b64decode(jsr.split(',')[1])
  jpgnp = np.frombuffer(iwizbyts, dtype=np.uint8)
  img = cv2.imdecode(jpgnp, flags=1)
  return img
def qb2byts(qbra):
  qbtablet = PIL.Image.fromarray(qbra, 'RGBA')
  strongEyes = io.BytesIO()
  qbtablet.save(strongEyes, format='png')
  qbbyts = 'data:image/png;base64,{}'.format((str(b64encode(strongEyes.getvalue()), 'utf-8')))
  return qbbyts


# Functions for starting Stream with Webcam
def video_frame(label, bbox):
  data = eval_js('stream_frame("{}", "{}")'.format(label, bbox))
  return data

def video_stream():
  js = Javascript('''
    var stream;
    var video;
    var rstrt;
    var iwizperiodic;
    var div = null;
    var unfinished = null;
    var stopp = false;
    var titleperiodic;

    function rmD() {
       stream.getVideoTracks()[0].stop();
       video.remove();
       div.remove();
       video = null;
       div = null;
       stream = null;
       iwizperiodic = null;
       rstrt = null;
       titleperiodic = null;
    }

    function animeFr() {
      if (!stopp) {
        window.requestAnimationFrame(animeFr);
      }
      if (unfinished) {
        var mark = "";
        if (!stopp) {
          rstrt.getContext('2d').drawImage(video, 0, 0, 640, 480);
          mark = rstrt.toDataURL('image/jpeg', 0.8)
        }
        var pl = unfinished;
        unfinished = null;
        pl(mark);
      }
    }

    async function crD() {
      if (div !== null) {
        return stream;
      }

      div = document.createElement('div');
      div.style.border = '2px solid black';
      div.style.padding = '3px';
      div.style.width = '100%';
      div.style.maxWidth = '600px';
      document.body.appendChild(div);

      const mohit = document.createElement('div');
      mohit.innerHTML = "<span>Status:</span>";
      titleperiodic = document.createElement('span');
      titleperiodic.innerText = 'No data';
      titleperiodic.style.fontWeight = 'bold';
      mohit.appendChild(titleperiodic);
      div.appendChild(mohit);

      video = document.createElement('video');
      video.style.display = 'block';
      video.width = div.clientWidth - 6;
      video.setAttribute('playsinline', '');
      video.onclick = () => { stopp = true; };
      stream = await navigator.mediaDevices.getUserMedia(
          {video: { facingMode: "environment"}});
      div.appendChild(video);

      iwizperiodic = document.createElement('img');
      iwizperiodic.style.position = 'absolute';
      iwizperiodic.style.zIndex = 1;
      iwizperiodic.onclick = () => { stopp = true; };
      div.appendChild(iwizperiodic);

      const instruction = document.createElement('div');
      instruction.innerHTML =
          '<span style="color: red; font-weight: bold;">' +
          'Click on the video or this text to end</span>';
      div.appendChild(instruction);
      instruction.onclick = () => { stopp = true; };

      video.srcObject = stream;
      await video.play();

      rstrt = document.createElement('canvas');
      rstrt.width = 640; //video.videoWidth;
      rstrt.height = 480; //video.videoHeight;
      window.requestAnimationFrame(animeFr);

      return stream;
    }
    async function stream_frame(label, imgData) {
      if (stopp) {
        rmD();
        stopp = false;
        return '';
      }

      var preCreate = Date.now();
      stream = await crD();

      var preShow = Date.now();
      if (label != "") {
        titleperiodic.innerHTML = label;
      }

      if (imgData != "") {
        var videoRect = video.getClientRects()[0];
        iwizperiodic.style.top = videoRect.top + "px";
        iwizperiodic.style.left = videoRect.left + "px";
        iwizperiodic.style.width = videoRect.width + "px";
        iwizperiodic.style.height = videoRect.height + "px";
        iwizperiodic.src = imgData;
      }

      var preCapture = Date.now();
      var mark = await new Promise(function(resolve, reject) {
        unfinished = resolve;
      });
      stopp = false;

      return {'create': preShow - preCreate,
              'show': preCapture - preShow,
              'capture': Date.now() - preCapture,
              'img': mark};
    }
    ''')

  display(js)

# Manipulates in the input data
def normalize(L):
  # given a list of numbers L, normalize it so all examples are
  # treated on a commensurate basis

  totalLength = 0
  centered_x = 0
  centered_y = 0

  for i in range(17):
    x_i = L[2 * i + 1]
    y_i = L[2 * i + 1 + 1]

    centered_x += x_i
    centered_y += y_i

  centered_x /= 17
  centered_y /= 17
  # print(str(centered_x) + " " + str(centered_y))

  for i in range(17):
    x_i = L[2 * i + 1] - centered_x
    y_i = L[2 * i + 1 + 1] - centered_y

    totalLength += np.sqrt(x_i**2 + y_i**2)

  answer = []
  answer.append(L[0])

  checkerLength = 0

  for i in range(17):
    x_i = L[2 * i + 1] - centered_x
    y_i = L[2 * i + 1 + 1] - centered_y

    localLength = np.sqrt(x_i**2 + y_i**2)
    vectorLength = localLength / totalLength

    unitVectorX_i = x_i / localLength
    unitVectorY_i = y_i / localLength

    answer.append(unitVectorX_i * vectorLength)
    answer.append(unitVectorY_i * vectorLength)
    checkerLength += vectorLength

  return answer

W = [-4.325657666816052, 0.08950988296523274, 0.2602615118602717, 0.09168778116347012, 0.2833736578201197, 0.08851209244449602, 0.2730213068764441, 0.03377786910176586, 0.2829417705077817, 0.044586852917931206, 0.28011183885977026, -0.056148143356378015, 0.18864196696604113, -0.02903514855283025, 0.19045440244384626, 0.018195586510948762, 0.01261177001665899, 0.03788696504963289, 0.03959836340755398, 0.12405132448563677, -0.0004533561232031207, 0.11884561233286743, 0.00893631774601232, -0.21652737025209765, -0.13717378206275407, -0.17609551346401248, -0.11537971424494572, 0.024653062721093397, -0.25369415095237674, 0.042377792711076015, -0.22879769502099515, -0.129253889915888, -0.5657603309523151, -0.10701182719630813, -0.5186349668198829]
P = [-3.416517163139581, -21.35578982291039, 15.294807287857722, -0.04446693184347948, 17.654806670742797, -21.405631908319723, 16.747640832754694, -0.006437738462491961, 11.96924658098809, -18.395037143828063, 10.38748343415219, -2.220676834411694, -2.7379735227710653, -1.887111081873324, -5.867522019037623, 10.692063278138463, 9.24797879387239, 8.8881291018652, 2.0018978882708645, 10.232955313849718, -16.92051006100624, 10.4495186854179, -13.42190284613647, -19.523003680479434, 16.79710045762282, 0.2498507719518179, 16.40767254150967, -17.499930083863376, 19.49555831355778, -0.4482036419241091, 19.620184048129254, -10.181590096181084, 15.884887923153764, -9.069319310498997, 15.56784735525869]
# we train S?
# W = []


# Computes the probability as a percent that the squat is good given a normalized L
def probability(L):
  dot_product = 0
  for i in range(0, 35):
    dot_product += L[i] * W[i]

  output = 1/(1 + np.exp(dot_product)) * 100
  output = (output - 99)/1 * 20 * 2.5 * 100

  if output < 0:
    output = 0

  if output > 100:
    output = 100

  return output

def probabilityPlank(L):
  dot_product = 0
  for i in range(0, 35):
    dot_product += L[i] * P[i]

  output = 1/(1 + np.exp(dot_product)) * 100

  return output

#Python Speech Function
def speak(text: str):
    tts = gTTS(text=text, lang="en")
    filename = "sound.mp3"
    tts.save(filename)
    Audio(filename, autoplay = True)

#Start Code
video_stream()
label_html = 'Live Stream is running...'
bbox = ''
count = 0
img_array = []
running_sum = 0
running_count = 0

while (time.time() < end_time):
    jsr = video_frame(label_html, bbox)
    if not jsr:
        break
    image = js2img(jsr["img"])
    # Resize and pad the image to keep the aspect ratio and fit the expected size.
    input_image = tf.expand_dims(image, axis=0)
    input_image = tf.image.resize_with_pad(input_image, input_size, input_size)

    # Run model inference.
    keypoints_with_scores = movenet(input_image)
    # print(keypoints_with_scores)

    # Visualize the predictions with image.
    display_image = tf.expand_dims(image, axis=0)
    display_image = tf.cast(tf.image.resize_with_pad(
        display_image, 1280, 1280), dtype=tf.int32)
    output_overlay = draw_prediction_on_image(
        np.squeeze(display_image.numpy(), axis=0), keypoints_with_scores)

    plt.figure(figsize=(5, 5))
    img_array.append(output_overlay)
    plt.imshow(output_overlay)

    keypointsxy = _keypoints_and_edges_for_display(keypoints_with_scores, 1280, 1280)[0]
    flattendList = []
    flattendList.append(1)

    for i in range(17):
      for j in range(2):
        if len(keypointsxy) > i:
          flattendList.append(keypointsxy[i][j])


    if len(flattendList) != 35:
      lastX = flattendList[len(flattendList)-2]
      lastY = flattendList[len(flattendList)-1]
      while len(flattendList) < 35:
        epsilon = np.random.rand()
        flattendList.append(lastX + epsilon)
        flattendList.append(lastY + epsilon)
    regularizedList = normalize(flattendList)
    goal = probability(regularizedList)
    print(goal)
    if goal > 30:
      running_count += 1
      running_sum += goal

    print(len(flattendList))
    print(flattendList)

    _ = plt.axis('off')
x = 0
if running_count != 0:
  x = float(running_sum/running_count)

val = str('%.2f'%(x))
text = "Your squat form was scored as " + val + " percent of perfection"
print(text)


for i in range(len(img_array)):
   img = img_array[i]
   height, width, layers = img.shape
   size = (width,height)
out = cv2.VideoWriter('video.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)




for i in range(len(img_array)):
   out.write(img_array[i])
out.release()

tts = gTTS(text=text, lang="en")
filename = "sound.mp3"
tts.save(filename)
Audio(filename, autoplay = True)

"""Run Program with Live Stream (plank)"""

#Variables Assignment
num_of_faces = 0
num_of_pictures_taken = 0
minutes_running = 3
end_time = time.time() + 60 * minutes_running

# function to convert the JavaScript object into an OpenCV image
def js2img(jsr):
  iwizbyts = b64decode(jsr.split(',')[1])
  jpgnp = np.frombuffer(iwizbyts, dtype=np.uint8)
  img = cv2.imdecode(jpgnp, flags=1)
  return img
def qb2byts(qbra):
  qbtablet = PIL.Image.fromarray(qbra, 'RGBA')
  strongEyes = io.BytesIO()
  qbtablet.save(strongEyes, format='png')
  qbbyts = 'data:image/png;base64,{}'.format((str(b64encode(strongEyes.getvalue()), 'utf-8')))
  return qbbyts


# Functions for starting Stream with Webcam
def video_frame(label, bbox):
  data = eval_js('stream_frame("{}", "{}")'.format(label, bbox))
  return data

def video_stream():
  js = Javascript('''
    var stream;
    var video;
    var rstrt;
    var iwizperiodic;
    var div = null;
    var unfinished = null;
    var stopp = false;
    var titleperiodic;

    function rmD() {
       stream.getVideoTracks()[0].stop();
       video.remove();
       div.remove();
       video = null;
       div = null;
       stream = null;
       iwizperiodic = null;
       rstrt = null;
       titleperiodic = null;
    }

    function animeFr() {
      if (!stopp) {
        window.requestAnimationFrame(animeFr);
      }
      if (unfinished) {
        var mark = "";
        if (!stopp) {
          rstrt.getContext('2d').drawImage(video, 0, 0, 640, 480);
          mark = rstrt.toDataURL('image/jpeg', 0.8)
        }
        var pl = unfinished;
        unfinished = null;
        pl(mark);
      }
    }

    async function crD() {
      if (div !== null) {
        return stream;
      }

      div = document.createElement('div');
      div.style.border = '2px solid black';
      div.style.padding = '3px';
      div.style.width = '100%';
      div.style.maxWidth = '600px';
      document.body.appendChild(div);

      const mohit = document.createElement('div');
      mohit.innerHTML = "<span>Status:</span>";
      titleperiodic = document.createElement('span');
      titleperiodic.innerText = 'No data';
      titleperiodic.style.fontWeight = 'bold';
      mohit.appendChild(titleperiodic);
      div.appendChild(mohit);

      video = document.createElement('video');
      video.style.display = 'block';
      video.width = div.clientWidth - 6;
      video.setAttribute('playsinline', '');
      video.onclick = () => { stopp = true; };
      stream = await navigator.mediaDevices.getUserMedia(
          {video: { facingMode: "environment"}});
      div.appendChild(video);

      iwizperiodic = document.createElement('img');
      iwizperiodic.style.position = 'absolute';
      iwizperiodic.style.zIndex = 1;
      iwizperiodic.onclick = () => { stopp = true; };
      div.appendChild(iwizperiodic);

      const instruction = document.createElement('div');
      instruction.innerHTML =
          '<span style="color: red; font-weight: bold;">' +
          'Click on the video or this text to end</span>';
      div.appendChild(instruction);
      instruction.onclick = () => { stopp = true; };

      video.srcObject = stream;
      await video.play();

      rstrt = document.createElement('canvas');
      rstrt.width = 640; //video.videoWidth;
      rstrt.height = 480; //video.videoHeight;
      window.requestAnimationFrame(animeFr);

      return stream;
    }
    async function stream_frame(label, imgData) {
      if (stopp) {
        rmD();
        stopp = false;
        return '';
      }

      var preCreate = Date.now();
      stream = await crD();

      var preShow = Date.now();
      if (label != "") {
        titleperiodic.innerHTML = label;
      }

      if (imgData != "") {
        var videoRect = video.getClientRects()[0];
        iwizperiodic.style.top = videoRect.top + "px";
        iwizperiodic.style.left = videoRect.left + "px";
        iwizperiodic.style.width = videoRect.width + "px";
        iwizperiodic.style.height = videoRect.height + "px";
        iwizperiodic.src = imgData;
      }

      var preCapture = Date.now();
      var mark = await new Promise(function(resolve, reject) {
        unfinished = resolve;
      });
      stopp = false;

      return {'create': preShow - preCreate,
              'show': preCapture - preShow,
              'capture': Date.now() - preCapture,
              'img': mark};
    }
    ''')

  display(js)

# Manipulates in the input data
def normalize(L):
  # given a list of numbers L, normalize it so all examples are
  # treated on a commensurate basis

  totalLength = 0
  centered_x = 0
  centered_y = 0

  for i in range(17):
    x_i = L[2 * i + 1]
    y_i = L[2 * i + 1 + 1]

    centered_x += x_i
    centered_y += y_i

  centered_x /= 17
  centered_y /= 17
  # print(str(centered_x) + " " + str(centered_y))

  for i in range(17):
    x_i = L[2 * i + 1] - centered_x
    y_i = L[2 * i + 1 + 1] - centered_y

    totalLength += np.sqrt(x_i**2 + y_i**2)

  answer = []
  answer.append(L[0])

  checkerLength = 0

  for i in range(17):
    x_i = L[2 * i + 1] - centered_x
    y_i = L[2 * i + 1 + 1] - centered_y

    localLength = np.sqrt(x_i**2 + y_i**2)
    vectorLength = localLength / totalLength

    unitVectorX_i = x_i / localLength
    unitVectorY_i = y_i / localLength

    answer.append(unitVectorX_i * vectorLength)
    answer.append(unitVectorY_i * vectorLength)
    checkerLength += vectorLength

  return answer

W = [-4.325657666816052, 0.08950988296523274, 0.2602615118602717, 0.09168778116347012, 0.2833736578201197, 0.08851209244449602, 0.2730213068764441, 0.03377786910176586, 0.2829417705077817, 0.044586852917931206, 0.28011183885977026, -0.056148143356378015, 0.18864196696604113, -0.02903514855283025, 0.19045440244384626, 0.018195586510948762, 0.01261177001665899, 0.03788696504963289, 0.03959836340755398, 0.12405132448563677, -0.0004533561232031207, 0.11884561233286743, 0.00893631774601232, -0.21652737025209765, -0.13717378206275407, -0.17609551346401248, -0.11537971424494572, 0.024653062721093397, -0.25369415095237674, 0.042377792711076015, -0.22879769502099515, -0.129253889915888, -0.5657603309523151, -0.10701182719630813, -0.5186349668198829]
P = [-3.416517163139581, -21.35578982291039, 15.294807287857722, -0.04446693184347948, 17.654806670742797, -21.405631908319723, 16.747640832754694, -0.006437738462491961, 11.96924658098809, -18.395037143828063, 10.38748343415219, -2.220676834411694, -2.7379735227710653, -1.887111081873324, -5.867522019037623, 10.692063278138463, 9.24797879387239, 8.8881291018652, 2.0018978882708645, 10.232955313849718, -16.92051006100624, 10.4495186854179, -13.42190284613647, -19.523003680479434, 16.79710045762282, 0.2498507719518179, 16.40767254150967, -17.499930083863376, 19.49555831355778, -0.4482036419241091, 19.620184048129254, -10.181590096181084, 15.884887923153764, -9.069319310498997, 15.56784735525869]
# we train S?
# W = []


# Computes the probability as a percent that the squat is good given a normalized L
def probability(L):
  dot_product = 0
  for i in range(0, 35):
    dot_product += L[i] * W[i]

  output = 1/(1 + np.exp(dot_product)) * 100
  output = (output - 99)/1 * 20 * 2.5 * 100

  if output < 0:
    output = 0

  if output > 100:
    output = 100

  return output

def probabilityPlank(L):
  dot_product = 0
  for i in range(0, 35):
    dot_product += L[i] * P[i]

  output = 1/(1 + np.exp(dot_product)) * 100

  return output

#Python Speech Function
def speak(text: str):
    tts = gTTS(text=text, lang="en")
    filename = "sound.mp3"
    tts.save(filename)
    Audio(filename, autoplay = True)

#Start Code
video_stream()
label_html = 'Live Stream is running...'
bbox = ''
count = 0
img_array = []
running_sum = 0
running_count = 0

while (time.time() < end_time):
    jsr = video_frame(label_html, bbox)
    if not jsr:
        break
    image = js2img(jsr["img"])
    # Resize and pad the image to keep the aspect ratio and fit the expected size.
    input_image = tf.expand_dims(image, axis=0)
    input_image = tf.image.resize_with_pad(input_image, input_size, input_size)

    # Run model inference.
    keypoints_with_scores = movenet(input_image)
    # print(keypoints_with_scores)

    # Visualize the predictions with image.
    display_image = tf.expand_dims(image, axis=0)
    display_image = tf.cast(tf.image.resize_with_pad(
        display_image, 1280, 1280), dtype=tf.int32)
    output_overlay = draw_prediction_on_image(
        np.squeeze(display_image.numpy(), axis=0), keypoints_with_scores)

    plt.figure(figsize=(5, 5))
    img_array.append(output_overlay)
    plt.imshow(output_overlay)

    keypointsxy = _keypoints_and_edges_for_display(keypoints_with_scores, 1280, 1280)[0]
    flattendList = []
    flattendList.append(1)

    for i in range(17):
      for j in range(2):
        if len(keypointsxy) > i:
          flattendList.append(keypointsxy[i][j])


    if len(flattendList) != 35:
      lastX = flattendList[len(flattendList)-2]
      lastY = flattendList[len(flattendList)-1]
      while len(flattendList) < 35:
        epsilon = np.random.rand()
        flattendList.append(lastX + epsilon)
        flattendList.append(lastY + epsilon)
    regularizedList = normalize(flattendList)
    goal = probabilityPlank(regularizedList)
    print(goal)
    if goal > 30:
      running_count += 1
      running_sum += goal

    print(len(flattendList))
    print(flattendList)

    _ = plt.axis('off')
x = 0
if running_count != 0:
  x = float(running_sum/running_count)

val = str('%.2f'%(x))
text = "Your plank form was scored as " + val + " percent of perfection"
print(text)


for i in range(len(img_array)):
   img = img_array[i]
   height, width, layers = img.shape
   size = (width,height)
out = cv2.VideoWriter('video.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)




for i in range(len(img_array)):
   out.write(img_array[i])
out.release()

tts = gTTS(text=text, lang="en")
filename = "sound.mp3"
tts.save(filename)
Audio(filename, autoplay = True)