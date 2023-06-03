import PropTypes from "prop-types";

const SubmitButton = ({ text }) => {
    return (
        <>
            <button className='bg-[#212121] h-[50px] w-[174px] text-white text-[1.3rem] font-black'>
                {text}
            </button>
        </>
    );
};

SubmitButton.propTypes = {
    text: PropTypes.string.isRequired,
};

export default SubmitButton;
