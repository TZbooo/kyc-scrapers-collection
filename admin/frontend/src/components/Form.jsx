import PropTypes from "prop-types";

const Form = ({ children, header, buttonText }) => {
    return (
        <>
            <div className='w-[100%] min-h-[100vh] bg-[#262626F2] flex justify-center items-center absolute py-[50px]'>
                <form className='bg-white p-[4.5rem] flex flex-col items-center gap-10 rounded-[5px]'>
                    <h1 className='font-semibold font-roboto text-[2.5rem] text-[#1D1D1D]'>
                        {header}
                    </h1>
                    <div className="flex flex-col gap-5">
                        {children}
                    </div>
                    <button className='bg-[#212121] h-[50px] w-[174px] text-white text-[1.3rem] font-black'>
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
