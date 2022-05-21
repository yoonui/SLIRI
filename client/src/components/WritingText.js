import React, {useState} from 'react'

function WritingText() {
    // eslint-disable-next-line
    const [text, setText] = useState("수어에 대한 자막");

  return (
    <div className="writngText">{text}</div>
  )
}

export default WritingText
