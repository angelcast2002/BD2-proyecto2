import React from "react";
import PropTypes from "prop-types";
import style from "./LoadButton.module.css";




const LoadButton = ({ onClick, text }) => {

  return (
    <button type="button" onClick={onClick} className={style.button}>
      {text}
    </button>
  );
}

export default LoadButton

