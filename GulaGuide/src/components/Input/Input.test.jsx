import React from "react"
import { test, it } from "vitest"
import Input from "./Input"

test("NumberButton Component", () => {
  it("Renders correctly", () => {
    render(<Input />)
  })
  it("should render input with correct props", () => {
    const wrapper = mount(
      <ComponentInput
        name="test"
        type="text"
        placeholder="test"
        onChange={() => {}}
        min={0}
        max={10}
        value=""
      />
    )
    const input = wrapper.find("input")
    expect(input.prop("name")).toEqual("test")
    expect(input.prop("type")).toEqual("text")
    expect(input.prop("placeholder")).toEqual("test")
    expect(input.prop("onChange")).toBeDefined()
    expect(input.prop("min")).toEqual(0)
    expect(input.prop("max")).toEqual(10)
  })
  it("should update input value when changed", () => {
    const onChange = jest.fn()
    const wrapper = mount(
      <ComponentInput
        name="test"
        type="text"
        placeholder="test"
        onChange={onChange}
        min={0}
        max={10}
        value=""
      />
    )
    const input = wrapper.find("input")
    input.simulate("change", { target: { value: "new value" } })
    expect(onChange).toHaveBeenCalled()
    expect(input.prop("value")).toEqual("new value")
  })
  it("should render input with empty value prop", () => {
    const wrapper = mount(
      <ComponentInput
        name="test"
        type="text"
        placeholder="test"
        onChange={() => {}}
        min={0}
        max={10}
        value=""
      />
    )
    const input = wrapper.find("input")
    expect(input.prop("value")).toEqual("")
  })
})
