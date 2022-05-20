import React from 'react'
import assistantLogo from "../assets/Google_Assistant_logo.png";
import WritingText from './WritingText';


function Chat() {
  return (
    <div className="section__assistant">
        <ul>
            <li>
                <img src={assistantLogo} className="assistant" alt={"구글 어시스턴트 로고"}/>
                <p>안녕하세요? 무엇을 도와드릴까요?</p>
            </li>
        </ul>
        <WritingText/>
    </div>
  )
}

export default Chat
