import PropTypes from "prop-types";
import EditIcon from "../assets/edit.svg";
import AddIcon from "../assets/add.svg";
import SimpleButton from "./Buttons/SimpleButton";

const ScraperTable = ({ name }) => {
    return (
        <>
            <div className='pt-[255px] px-[60px] pb-[60px]'>
                <div className='flex flex-col gap-2'>
                    <h3 className='font-black text-[#828282] text-[45px]'>
                        {name}
                    </h3>
                    <div className='flex flex-col gap-[60px]'>
                        <div className='flex flex-col gap-[15px]'>
                            <div className='h-[116px] w-[100%] border-[#ABABAB] border-[1px] px-[38px] flex justify-between items-center font-semibold font-roboto text-[1.3vw] leading-[28.13px]'>
                                <div className='h-[56px] w-[10vw] flex items-center'>
                                    Телеграм каналы
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center'>
                                    Всего взаимодействий
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center'>
                                    За месяц взаимодействий
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center'>
                                    За сегодня взаимодествий
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center'>
                                    Информационный источник
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center'>
                                    Запуск
                                </div>
                            </div>
                            <div className='h-[184px] w-[100%] border-[#ABABAB] border-[1px] px-[38px] flex justify-between items-center font-roboto'>
                                <div className='h-[56px] flex items-center font-medium text-[1.1vw]'>
                                    Название тг канала
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                                    1234
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                                    1234
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                                    1234
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                                    Название
                                </div>
                                <div className='w-[10vw] flex flex-col gap-[10px]'>
                                    <SimpleButton>
                                        Запустить
                                    </SimpleButton>
                                    <div className='flex justify-between'>
                                        <div className='rounded-[3px] border-[#212121] border-[1px] py-[10px] pl-[12px] pr-[11px]'>
                                            <img src={EditIcon} />
                                        </div>
                                        <span className='font-medium underline flex items-center'>
                                            Удалить
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div className='h-[184px] w-[100%] border-[#ABABAB] border-[1px] px-[38px] flex justify-between items-center font-roboto'>
                                <div className='h-[56px] flex items-center font-medium text-[1.1vw]'>
                                    Название тг канала
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                                    1234
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                                    1234
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                                    1234
                                </div>
                                <div className='h-[56px] w-[10vw] flex items-center font-normal text-[1.1vw] leading-[21.09px]'>
                                    Название
                                </div>
                                <div className='w-[10vw] flex flex-col gap-[10px]'>
                                    <SimpleButton filled={true}>
                                        <span>Остановить</span>
                                    </SimpleButton>
                                    <div className='flex justify-between'>
                                        <div className='rounded-[3px] border-[#212121] border-[1px] py-[10px] pl-[12px] pr-[11px]'>
                                            <img src={EditIcon} />
                                        </div>
                                        <span className='font-medium underline flex items-center'>
                                            Удалить
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="px-[42px] flex justify-between">
                            <SimpleButton filled={true}>
                                <img src={AddIcon} />
                                <span>Добавить</span>
                            </SimpleButton>
                            <SimpleButton filled={true}>
                                Остановить все
                            </SimpleButton>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

ScraperTable.propTypes = {
    name: PropTypes.string.isRequired,
};

export default ScraperTable;
