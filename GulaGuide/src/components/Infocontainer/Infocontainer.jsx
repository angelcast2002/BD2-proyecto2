import React from "react"
import PropTypes from "prop-types"
import styles from "./Infocontainer.module.css"

const Infocontainer = ({ text, backgroundColor, textColor, title }) => {
  return (
    <div
      style={{
        backgroundColor,
        color: textColor,
      }}
      className={styles.infocontainer}
    >
      <h1>{title}</h1>
      {text}
    </div>
  )
}

Infocontainer.propTypes = {
  text: PropTypes.string.isRequired,
  backgroundColor: PropTypes.string.isRequired,
  textColor: PropTypes.string.isRequired,
}

export default Infocontainer
