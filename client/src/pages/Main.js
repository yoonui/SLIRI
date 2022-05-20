  // eslint-disable-next-line
import React,{useEffect, useState} from 'react';
import MPHands from "../components/MPHands";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUsers } from "@fortawesome/free-solid-svg-icons";
import {Helmet} from "react-helmet";
  // eslint-disable-next-line
import axios from 'axios';

import '../App.css';
import Chat from '../components/Chat';

function Main() {
  // eslint-disable-next-line
  const [value, setValue] = useState("");

  useEffect(() => {
    axios
      .get("http://localhost:5000/text")
      .then((res) => {
        console.log(res);
      }
    );
  });

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
          </div>
          <Chat/>
        </div>
      </div>
    </div>
        </> 
  );
}

export default Main;
