import PropTypes from "prop-types";

const TextInput = ({ value, valueSetter, placeholder, inputType }) => {
    return (
        <input
            value={value}
            onChange={(e) => valueSetter(e.target.value)}
            className='bg-[#F0F0F0] border-[#C9C9C9] border-[1px] h-[3.5em] w-[705px] rounded-[8px] px-5 font-roboto text-[#1D1D1D]'
            placeholder={placeholder}
            type={inputType}
        />
    );
};

TextInput.defaultProps = {
    inputType: "text",
};

TextInput.propTypes = {
    value: PropTypes.string.isRequired,
    valueSetter: PropTypes.func.isRequired,
    placeholder: PropTypes.string.isRequired,
    inputType: PropTypes.oneOf(["text", "password", "email"]),
};

export default TextInput;
