import React from "react"
import PropTypes from "prop-types"
import style from "./Message.module.css"
import { format } from "date-fns"

const Message = ({ pfp, name, time, message, file, side, nameColor, timeColor }) => {
  const formatTime = time
    ? format(new Date(time), "dd/MM/yyyy hh:mm a")
    : "07/11/2024 11:28 PM"

  return (
    <div
      className={
        side === "right" ? style.messageContainer : style.messageContainerLeft
      }
      style={{ alignItems: side === "right" ? "flex-end" : "flex-start" }}
    >
      <div className={style.header}>
        {side === "left" ? (<div className={style.pfp}>
          <img src={pfp} alt={name} />
        </div>) : null}
        <div
          className={style.chatInfo}
          style={{
            alignItems: side === "right" ? "flex-end" : "flex-start",
          }}
        >
          <div className={style.name} style={{color: nameColor ? nameColor : ""}}>{name}</div>
          {time ? (<div className={style.time} style={{color: timeColor ? timeColor : ""}}>{formatTime}</div>): null}
        </div>
        {side === "right" ? (<div className={style.pfp}>
          <img src={pfp} alt={name} />
        </div>) : null}
      </div>
      <div className={style.content}>
        {message.length > 0 ? (
          <div
            className={style.message}
            style={{
              backgroundColor: side === "right" ? "#13a2ef" : "#b15fbc",
            }}
          >
            {message}
          </div>
        ) : (
          <img src={file} className={style.file} alt={name} />
        )}
      </div>
    </div>
  )
}

Message.propTypes = {
  pfp: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  time: PropTypes.string.isRequired,
  message: PropTypes.string.isRequired,
  file: PropTypes.string.isRequired,
  side: PropTypes.string.isRequired,
}

export default Message
