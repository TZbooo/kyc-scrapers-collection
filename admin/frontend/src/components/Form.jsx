import PropTypes from 'prop-types';

const Form = ({ children }) => {
    return (
        <>
            <div className='w-[100vw] h-[100vh] bg-[#262626F2] flex justify-center items-center absolute'>
                <form className='bg-white p-[4.5em] inline-flex flex-col items-center gap-[2.5em] rounded-[5px]'>
                    {children}
                </form>
            </div>
        </>
    );
};

Form.propTypes = {
    children: PropTypes.node.isRequired
}

export default Form;
