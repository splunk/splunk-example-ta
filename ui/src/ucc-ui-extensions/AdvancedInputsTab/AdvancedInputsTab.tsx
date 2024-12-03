import React from "react";
import Table from "@splunk/react-ui/Table";

import { SplunkThemeProvider, variables } from "@splunk/themes";
import styled from "styled-components";
import { useGetRequest } from "../../utils/apiHooks.ts";

const HostStyles = styled.div`
  padding: ${variables.spacingLarge} 0;
`;

interface InputResponse {
  entry: {
    name: string;
    content: {
      account: string;
      disabled: boolean;
      fetch_from: string;
      index: string;
      interval: string;
    };
  }[];
}

export function AdvancedInputsTab() {
  const { data, isLoaded } = useGetRequest<InputResponse>({
    endpointUrl: "Splunk_TA_Example_example",
  });
  const inputs = data?.entry;

  return (
    <SplunkThemeProvider>
      <HostStyles>
        {isLoaded && (
          <Table>
            <Table.Head>
              <Table.HeadCell>Name</Table.HeadCell>
              <Table.HeadCell align="right">Interval</Table.HeadCell>
              <Table.HeadCell>Account</Table.HeadCell>
            </Table.Head>
            <Table.Body>
              {inputs?.map((row) => (
                <Table.Row key={row.name} disabled={row.content.disabled}>
                  <Table.Cell>{row.name}</Table.Cell>
                  <Table.Cell align="right">{row.content.interval}</Table.Cell>
                  <Table.Cell>{row.content.account}</Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table>
        )}
      </HostStyles>
    </SplunkThemeProvider>
  );
}
