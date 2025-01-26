import { SummaryResponse } from "../interfaces/SummaryResponse";

interface Props {
    response: SummaryResponse;
}

const SummaryTable = ({ response: { details, experience_level } }: Props) => {
    return (
        <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead>
                <tr className="bg-gray-100">
                    <th className="border border-gray-300 px-4 py-2">Type</th>
                    <th className="border border-gray-300 px-4 py-2">Values</th>
                </tr>
            </thead>
            <tbody>
                {details.full_name && (
                    <tr>
                        <td className="border border-gray-300 px-4 py-2">
                            Full Name
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                            {details.full_name}
                        </td>
                    </tr>
                )}
                {details.email && (
                    <tr>
                        <td className="border border-gray-300 px-4 py-2">
                            Email
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                            {details.email}
                        </td>
                    </tr>
                )}
                {details.phone_number && (
                    <tr>
                        <td className="border border-gray-300 px-4 py-2">
                            Phone number
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                            {details.phone_number}
                        </td>
                    </tr>
                )}

                {details.experience && (
                    <tr>
                        <td className="border border-gray-300 px-4 py-2">
                            Project(s)
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                            Worked on{" "}
                            {details.experience.map((name, index) => (
                                <span key={index}>
                                    {name}
                                    {index < details.experience!.length - 1 &&
                                        ", "}
                                </span>
                            ))}
                        </td>
                    </tr>
                )}
                {details.education && (
                    <tr>
                        <td className="border border-gray-300 px-4 py-2">
                            School(s)
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                            {details.education.map((name, index) => (
                                <span key={index}>
                                    {name}
                                    {index < details.education!.length - 1 &&
                                        ", "}
                                </span>
                            ))}
                        </td>
                    </tr>
                )}
                {details.languages_spoken && (
                    <tr>
                        <td className="border border-gray-300 px-4 py-2">
                            Languages(s)
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                            {details.languages_spoken.map((name, index) => (
                                <span key={index}>
                                    {name}
                                    {index <
                                        details.languages_spoken!.length - 1 &&
                                        ", "}
                                </span>
                            ))}
                        </td>
                    </tr>
                )}
                {experience_level && (
                    <tr>
                        <td className="border border-gray-300 px-4 py-2">
                            Level
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                            {experience_level}
                        </td>
                    </tr>
                )}
                {details.skills && (
                    <tr>
                        <td className="border border-gray-300 px-4 py-2">
                            Skills(s)
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                            <ul className="list-disc list-inside grid grid-cols-3 gap-4">
                                {details.skills.map((name, index) => (
                                    <li key={index}>{name}</li>
                                ))}
                            </ul>
                        </td>
                    </tr>
                )}
            </tbody>
        </table>
    );
};

export default SummaryTable;
