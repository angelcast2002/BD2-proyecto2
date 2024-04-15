import Input from "./Input"

export default {
  title: "Components/Input",
  component: Input,
  tags: ["autodocs"],
  argTypes: {},
}

export const asText = {
  args: {
    name: "username",
    value: "",
    onChange: () => {},
    type: "text",
    placeholder: "Ejemplo",
  },
}

export const asPassword = {
  args: {
    name: "password",
    value: "",
    onChange: () => {},
    type: "password",
    placeholder: "",
  },
}

export const asNumber = {
  args: {
    name: "carnet",
    value: "",
    onChange: () => {},
    type: "number",
    placeholder: "",
  },
}
