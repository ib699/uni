library ieee;
use ieee.std_logic_1164.all;
entity VENDING is
	port(CLK: in std_logic;
		RST: in std_logic;
		D, P: in std_logic;
		DOOR: out std_logic);
end VENDING;
--
architecture RTL of VENDING is
	type ST_TYPE is (START, P200, P400, FULL);
	signal CUR, NXT: ST_TYPE;
begin
--
	process(CLK)
	begin
		if rising_edge(CLK) then
			if RST = '1' then
				CUR <= START;
			else
				CUR <= NXT;
			end if;
		end if;
	end process;
--
	process(CUR, D, P)
		variable DP: std_logic_vector(1 downto 0) := (D, P);
	begin
		case CUR is
			when START =>
				if DP = "00" then
					NXT <= START;
				elsif DP = "01" then
					NXT <= FULL;
				else
					NXT <= P200;
				end if;
			when P200 =>
				if DP = "00" then
					NXT <= P200;
				elsif DP = "01" then
					NXT <= FULL;
				else
					NXT <= P400;
				end if;
			when P400 =>
				if DP = "00" then
					NXT <= P400;
				else
					NXT <= FULL;
				end if;
			when FULL =>
				NXT <= FULL;
		end case;
	end process;
--
	process(CUR, D, P)
		variable DP: std_logic_vector(1 downto 0) := (D, P);
	begin
		case CUR is
			when START =>
				if P = '0' then
					DOOR <= '0';
				else
					DOOR <= '1';
				end if;
			when P200 =>
				if P = '0' then
					DOOR <= '0';
				else
					DOOR <= '1';
				end if;
			when P400 =>
				if DP = "00" or DP = "11" then
					DOOR <= '0';
				else
					DOOR <= '1';
				end if;
			when FULL =>
					DOOR <= '0';
		end case;
	end process;
--
end RTL;
