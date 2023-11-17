type Props = Readonly<{
    icon: string;
    alt: string;
}>;

export const Icon = ({ icon, alt }: Props) => {
    return <img src={icon} alt={alt} width={40} />;
};
