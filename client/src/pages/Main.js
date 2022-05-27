  // eslint-disable-next-line
  import React,{useEffect, useState} from 'react';
  import MPHands from "../components/MPHands";
  import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
  import { faUsers } from "@fortawesome/free-solid-svg-icons";
  import {Helmet} from "react-helmet";
    // eslint-disable-next-line
  import axios from 'axios';
  import image from './image.png';
  
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
        <img style={{display:"block", margin:"auto", width:"100%", height:"100%"}}src={image} alt="SLIRI 배경"/>
      </> 
    );
  }
  
  export default Main;
  