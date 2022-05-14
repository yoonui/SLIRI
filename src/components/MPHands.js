import React from "react";
import { Hands } from "@mediapipe/hands";
import {Camera} from "@mediapipe/camera_utils";
import Webcam from "react-webcam";
import drawUtils from '@mediapipe/drawing_utils';
// eslint-disable-next-line
import {useRef, useEffect} from 'react';
import axios from 'axios';

let num = 0;

const MPHands = () => {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);

  function onResults(results){

    // eslint-disable-next-line
    let timerId = setInterval(() => {
    const r1 = results['multiHandLandmarks'][0];
    const r2 = results['multiHandWorldLandmarks'][0];
    const r3 = results['multiHandedness'][0];

    // eslint-disable-next-line
    const response = axios.get("http://localhost:5000/myhand", {params:{num:num, hands1:r1, hands2:r2, hands3:r3}});
    // console.log(response);
    // console.log(response.data);

    console.log(results);
    num++;
    
  }, 2000);

    //setting height, width of Canvas
    canvasRef.current.width = webcamRef.current.video.videoWidth;
    canvasRef.current.height = webcamRef.current.video.videoHeight;

    const canvasElement = canvasRef.current;
    const canvasCtx = canvasElement.getContext("2d");
    canvasCtx.clearRect(0, 0, canvasElement.wdith, canvasElement.height);
    canvasCtx.drawImage(
      results.image, 0, 0, canvasElement.width, canvasElement.height);
      if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
          drawUtils.drawConnectors(canvasCtx, landmarks, Hands.HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 5});
          drawUtils.drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2});
        }
      }
      canvasCtx.restore();
  }

  useEffect(() => {
    const hands = new Hands({
      locateFile : (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
      }
    })
    hands.setOptions({
      maxNumHands: 2,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
      selfieMode: true
    })
    hands.onResults(onResults);

    if(typeof webcamRef.current != "undefined" && webcamRef.current != null){
      const camera = new Camera(webcamRef.current.video, {
        onFrame: async() => {
          await hands.send({image:webcamRef.current.video})
        },
        width: 640,
        height: 480
      });
      camera.start();
    }
  });

    return (
    <>
      <Webcam
        ref={webcamRef}
        style={{
            position: "absolute",
            marginRight: "auto",
            marginLeft: "auto",
            left: 0,
            right: 0,
            textAlign: "center",
            zIndex: 9,
            width: 640,
            height: 480
        }}
      />
    <canvas
      ref={canvasRef}
      style={{
        position: "absolute",
        marginRight: "auto",
        marginLeft: "auto",
        left: 0,
        right: 0,
        textAlign: "center",
        zIndex: 9,
        width: 640,
        height: 480
      }}
    >
    </canvas>
        </>
    )
}

export default MPHands;