import PropTypes from "prop-types";

const SimpleButton = ({ children, filled, handleClick }) => {
    return (
        <>
            {filled ? (
                <button onClick={handleClick} className='bg-[#212121] text-white font-semibold rounded-[3px] py-[12px] px-[30px] flex gap-[11px] items-center justify-center'>
                    {children}
                </button>
            ) : (
                <button onClick={handleClick} className='font-semibold rounded-[3px] border-[#212121] border-[1px] py-[12px] px-[30px]'>
                    {children}
                </button>
            )}
        </>
    );
};

SimpleButton.defaultProps = {
    filled: false,
};

SimpleButton.propTypes = {
    children: PropTypes.element.isRequired,
    filled: PropTypes.bool,
    handleClick: PropTypes.func
};

export default SimpleButton;
