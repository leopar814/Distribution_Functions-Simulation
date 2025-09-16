import { BlockMath } from 'react-katex';

export default function Header({ distributionName, formula }) {

    return (
        <header className="flex flex-col w-full bg-gray-100 justify-center items-center pt-6 px-6 header">
            <h1 className="text-5xl font-bold mb-2">{distributionName}</h1>
            <div className="text-xl">
                <BlockMath 
                    math={formula} 
                />
            </div>
        </header>

    );

}