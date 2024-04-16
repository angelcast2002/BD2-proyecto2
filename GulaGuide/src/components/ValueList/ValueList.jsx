import React from "react"
import Select from "@mui/joy/Select"
import Option from "@mui/joy/Option"

const ValueList = ({
  value,
  placeholder,
  options,
  size="md",
  variant="soft",
  onChange,
  multiple=false
}) => {
  return (
    <Select
      multiple={multiple}
      size={size}
      defaultValue={value}
      placeholder={placeholder}
      variant={variant}
      onChange={onChange}
    >
      {options.map((option) => (
        <Option key={option} value={option}>
          {option}
        </Option>
      ))}
    </Select>
  )
}

export default ValueList
