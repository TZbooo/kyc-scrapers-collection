import PropTypes from "prop-types";
import CancelButton from "../Buttons/CancelFormButton";
import SubmitButton from "../Buttons/SubmitButton";

const Form = ({ children, header, buttonText }) => {
    return (
        <>
            <div className='w-[100%] min-h-[100vh] bg-[#262626F2] flex justify-center items-center fixed py-[50px]'>
                <form className='w-[62vw] bg-white p-[40px] pb-[100px] flex flex-col items-center gap-[38px] rounded-[5px]'>
                    <CancelButton />
                    <div className="flex flex-col items-center gap-[32px]">
                        <h1 className='font-semibold font-roboto text-[30px] text-[#1D1D1D]'>
                            {header}
                        </h1>
                        <div className="flex flex-col items-center gap-[30px]">
                            <div className='flex flex-col gap-5'>{children}</div>
                            <SubmitButton>{buttonText}</SubmitButton>
                        </div>
                    </div>
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
