import React from 'react';
import MPHands from "./components/MPHands";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUsers } from "@fortawesome/free-solid-svg-icons";
import {Helmet} from "react-helmet";
import assistantLogo from "./assets/Google_Assistant_logo.png";

import './App.css';

function App() {
  return (
    <>
         <Helmet>
                <meta charSet={"utf-8"}/>
                <title>SLIRI</title>
            </Helmet>
          <div>
      <div>
        <div className="background">
          <div className="section__webcam">
            <div className="title">
              <h2>SLIRI</h2>
              <FontAwesomeIcon icon={faUsers} />
            </div>
            <MPHands/>
            <div className="desc">(수어에 대한 자막)</div>
          </div>
          <div className="section__assistant">
            <ul>
              <li>
                <img src={assistantLogo} className="assistant" alt={"구글 어시스턴트 로고"}/>
                <p>안녕하세요? 무엇을 도와드릴까요?</p>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
        </> 
  );
}

export default App;
