import PropTypes from "prop-types";

const TextInput = ({
    value,
    valueSetter,
    error,
    placeholder,
    type,
}) => {
    return (
        <>
            <div className='flex flex-col gap-2'>
                <input
                    value={value}
                    onChange={(e) => valueSetter(e.target.value)}
                    className='bg-[#F0F0F0] border-[#C9C9C9] border-[1px] h-[55px] w-[705px] rounded-[8px] px-5 font-roboto text-[#1D1D1D]'
                    placeholder={placeholder}
                    type={type}
                />
                {error ? <span className='ml-1 font-roboto text-[#9b3434]'>{error}</span> : <></>}
            </div>
        </>
    );
};

TextInput.defaultProps = {
    type: "text",
};

TextInput.propTypes = {
    value: PropTypes.string.isRequired,
    valueSetter: PropTypes.func.isRequired,
    error: PropTypes.string.isRequired,
    placeholder: PropTypes.string.isRequired,
    type: PropTypes.oneOf(["text", "number", "password", "email"]),
};

export default TextInput;
