import PropTypes from "prop-types";

const Form = ({ children, header, buttonText }) => {
    return (
        <>
            <div className='w-[100vw] h-[100vh] bg-[#262626F2] flex justify-center items-center absolute'>
                <form className='bg-white p-[4.5em] inline-flex flex-col items-center gap-[2.5em] rounded-[5px]'>
                    <h1 className='font-semibold font-roboto text-[2.5em] text-[#1D1D1D]'>
                        {header}
                    </h1>
                    <div className="flex flex-col gap-5">
                        {children}
                    </div>
                    <button className='bg-[#212121] h-[2.9em] w-[174px] text-white text-[1.3em] font-black'>
                        {buttonText}
                    </button>
                </form>
            </div>
        </>
    );
};

Form.propTypes = {
    children: PropTypes.element.isRequired,
    header: PropTypes.string.isRequired,
    buttonText: PropTypes.string.isRequired,
};

export default Form;
