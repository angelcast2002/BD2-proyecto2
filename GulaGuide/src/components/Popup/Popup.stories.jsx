import Popup from "./Popup"

export default {
  title: "Output/PopUp",
  component: Popup,
  tags: ["autodocs"],
  argTypes: {},
}

export const asError = {
  args: {
    message: "Algo ha fallado",
    status: true,
    style: 1,
  },
}

export const asWarning = {
  args: {
    message: "Algo ha fallado",
    status: true,
    style: 2,
  },
}

export const asOk = {
  args: {
    message: "Algo ha fallado",
    status: true,
    style: 3,
  },
}
