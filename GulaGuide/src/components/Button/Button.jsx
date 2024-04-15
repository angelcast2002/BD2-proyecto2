import React from "react"
import PropTypes from "prop-types"
import style from "./Button.module.css"

const Button = ({
  label,
  backgroundColor,
  textColor,
  onClick,
  noborder,
  test,
}) => (
  <div className={style.buttonContainer}>
    <button
      type="button"
      data-testid={test}
      style={
        noborder
          ? { backgroundColor, color: textColor, border: "none" }
          : { backgroundColor, color: textColor }
      }
      onClick={onClick}
    >
      {label}
    </button>
  </div>
)

Button.propTypes = {
  label: PropTypes.string.isRequired,
  backgroundColor: PropTypes.string,
  textColor: PropTypes.string,
  onClick: PropTypes.func.isRequired,
  noborder: PropTypes.bool,
  test: PropTypes.string.isRequired,
}

Button.defaultProps = {
  backgroundColor: "#fff",
  textColor: "#000",
  noborder: false,
}

export default Button
