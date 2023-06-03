import PropTypes from "prop-types";

const SubmitButton = ({ children }) => {
    return (
        <>
            <button className='bg-[#212121] px-[29px] py-[20px] text-white text-[22px] leading-[35px] font-black'>
                {children}
            </button>
        </>
    );
};

SubmitButton.propTypes = {
    children: PropTypes.element.isRequired,
};

export default SubmitButton;
