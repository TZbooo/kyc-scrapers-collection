import PropTypes from "prop-types";
import CancelFormButton from "../Buttons/CancelFormButton";
import SubmitButton from "../Buttons/SubmitButton";

const Form = ({
    children,
    header,
    buttonText,
    handleSubmit,
    disable,
    disableSetter,
}) => {
    if (!disable) {
        return (
            <>
                <div className='w-[100%] min-h-[100vh] bg-[#262626F2] flex justify-center items-center fixed top-0 left-0 py-[50px]'>
                    <form
                        onSubmit={handleSubmit}
                        className='w-[62vw] bg-white p-[40px] pb-[100px] flex flex-col items-center gap-[38px] rounded-[5px]'
                    >
                        <CancelFormButton
                            handleClick={() => disableSetter(true)}
                        />
                        <div className='flex flex-col items-center gap-[32px]'>
                            <h1 className='font-semibold font-roboto text-[30px] text-[#1D1D1D]'>
                                {header}
                            </h1>
                            <div className='flex flex-col items-center gap-[30px]'>
                                <div className='flex flex-col gap-5'>
                                    {children}
                                </div>
                                <SubmitButton>{buttonText}</SubmitButton>
                            </div>
                        </div>
                    </form>
                </div>
            </>
        );
    }
};

Form.propTypes = {
    children: PropTypes.element.isRequired,
    header: PropTypes.string.isRequired,
    buttonText: PropTypes.string.isRequired,
    handleSubmit: PropTypes.func.isRequired,
    disable: PropTypes.bool,
    disableSetter: PropTypes.func,
};

export default Form;
