import React, { useState } from "react"
import PropTypes from "prop-types"
import styles from "./Input.module.css"

// eslint-disable-next-line react/prop-types
const ComponentInput = ({
  name,
  type,
  placeholder,
  onChange,
  min,
  max,
  value,
  eye,
  isOpen,
  onClickButton,
}) => {
  if(eye){
    if(isOpen){
      return (
        <div className={styles.inputContainer}>
          <input
            value={value}
            id={name}
            name={name}
            type="text"
            placeholder={placeholder}
            onChange={onChange}
            min={min}
            max={max}
          />
          <button className={styles.eyeContainer} onClick={onClickButton}>
            <img src="/images/openEye.svg" alt="eye" />
          </button>
        </div>
      )
    } else {
      return (
        <div className={styles.inputContainer}>
          <input
            value={value}
            id={name}
            name={name}
            type="password"
            placeholder={placeholder}
            onChange={onChange}
            min={min}
            max={max}
          />
          <button className={styles.eyeContainer} onClick={onClickButton}>
            <img src="/images/closedEye.svg" alt="eye" />
          </button>
        </div>
      )
    }
  } else {
    return (
      <div className={styles.inputContainer}>
        <input
          value={value}
          id={name}
          name={name}
          type={type}
          placeholder={placeholder}
          onChange={onChange}
          min={min}
          max={max}
        />
      </div>
    )
  }
}

ComponentInput.propTypes = {
  name: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  placeholder: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
}

export default ComponentInput
