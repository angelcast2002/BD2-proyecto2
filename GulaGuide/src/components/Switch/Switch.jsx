import React from "react";
import "./Switch.css";

const Switch = ({ onClick, value }) => {
  return (
    <div class="wrapper">
        <div class="card-switch">
            <label class="switch">
               <input type="checkbox" class="toggle" onClick={onClick} value={value} />
               <span class="slider"></span>
               <span class="card-side"></span>
            </label>
        </div>   
   </div>
  )
}

export default Switch