import PropTypes from "prop-types";
import AddIcon from "../assets/add.svg";
import SimpleButton from "./Buttons/SimpleButton";
import TableHeaders from "./Table/TableHeaders";
import TableItem from "./Table/TableItem";
import EditScraperForm from "./Forms/EditScraperForm";

const ScraperTable = ({ name, headers }) => {
    return (
        <>
            <EditScraperForm />
            <div className='pt-[255px] px-[60px] pb-[60px]'>
                <div className='flex flex-col gap-2'>
                    <h3 className='font-black text-[#828282] text-[45px]'>
                        {name}
                    </h3>
                    <div className='flex flex-col gap-[60px]'>
                        <div className='flex flex-col gap-[15px]'>
                            <TableHeaders headers={headers} />
                            <TableItem
                                name='Название тг канала'
                                total={1234}
                                totalPerMonth={1234}
                                totalPerDay={1234}
                                origin='https://t.me/example'
                                isRunning={false}
                            />
                            <TableItem
                                name='Название тг канала'
                                total={1234}
                                totalPerMonth={1234}
                                totalPerDay={1234}
                                origin='https://t.me/example'
                                isRunning={true}
                            />
                        </div>
                        <div className='px-[42px] flex justify-between'>
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
    headers: PropTypes.array.isRequired,
};

export default ScraperTable;
