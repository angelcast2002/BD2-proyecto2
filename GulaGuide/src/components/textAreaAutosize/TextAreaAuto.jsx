import React from "react"
import PropTypes from "prop-types"
import TextareaAutosize from "react-textarea-autosize"
import styles from "./TextAreaAuto.module.css"

// eslint-disable-next-line react/prop-types
const TextArea = ({
  name,
  type,
  placeholder,
  onChange,
  minRows,
  maxRows,
  value,
}) => {
  return (
    <div className={styles.inputContainer}>
      <TextareaAutosize
        className={styles.textArea}
        value={value}
        id={name}
        name={name}
        type={type}
        placeholder={placeholder}
        onChange={onChange}
        minRows={minRows}
        maxRows={maxRows}
      />
    </div>
  )
}

TextArea.propTypes = {
  name: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  placeholder: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
}

export default TextArea
